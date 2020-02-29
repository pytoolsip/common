# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-13 23:07:38
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2020-02-05 21:17:20

import wx;

from _Global import _GG;
from function.base import *;

class AboutIPDialogUI(wx.Dialog):
	"""docstring for AboutIPDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(AboutIPDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = AboutIPDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "关于平台",
			"size" : (-1,-1),
			"style" : wx.DEFAULT_DIALOG_STYLE,
			"blurUrlColor" : wx.Colour(60,60,240),
			"focusUrlColor" : wx.Colour(60,60,140),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initDialog(self):
		self.createControls(); # 创建控件
		self.initDialogLayout(); # 初始化布局
		self.updatePosition(); # 更新位置

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***Dialog"); # , parent = self, params = {}
		self.createContent();
		self.createAPPTitle();
		self.createCopyrightInfo();
		
	def initDialogLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__appTitle, flag = wx.ALIGN_CENTER|wx.ALL, border = 20);
		box.Add(self.__content, flag = wx.ALIGN_CENTER|wx.ALL, border = 10);
		box.Add(self.__copyrightInfo, flag = wx.ALIGN_CENTER|wx.ALL, border = 10);
		self.SetSizerAndFit(box);

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]/2));

	def updateDialog(self, data):
		pass;

	def createContent(self):
		self.__content = wx.Panel(self);
		self.createVersionView(self.__content);
		self.createWebsiteView(self.__content);
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__version, flag = wx.TOP|wx.BOTTOM, border = 5);
		box.Add(self.__website, flag = wx.TOP|wx.BOTTOM, border = 5);
		self.__content.SetSizerAndFit(box);


	def createVersionView(self, parent):
		self.__version = wx.Panel(parent);
		title = wx.StaticText(self.__version, label = "版本号：");
		title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		val = wx.StaticText(self.__version, label = _GG("ClientConfig").UrlConfig().GetIPVersion());
		val.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		val.SetForegroundColour(wx.Colour(0,100,0));
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(title, flag = wx.ALIGN_CENTER|wx.RIGHT, border = 5);
		box.Add(val, flag = wx.ALIGN_CENTER);
		self.__version.SetSizerAndFit(box);

	def createWebsiteView(self, parent):
		self.__website = wx.Panel(parent);
		title = wx.StaticText(self.__website, label = "官网：");
		title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		url = wx.StaticText(self.__website, label = _GG("AppConfig")["PyToolsIPUrl"]);
		url.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, underline = True));
		url.SetForegroundColour(self.__params["blurUrlColor"]);
		url.Bind(wx.EVT_ENTER_WINDOW, self.onEnterUrl);
		url.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaveUrl);
		url.Bind(wx.EVT_LEFT_DOWN, self.onClickUrl);
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(title, flag = wx.ALIGN_CENTER|wx.RIGHT, border = 5);
		box.Add(url, flag = wx.ALIGN_CENTER);
		self.__website.SetSizerAndFit(box);

	def onEnterUrl(self, event):
		event.GetEventObject().SetForegroundColour(self.__params["focusUrlColor"]);
		event.GetEventObject().Refresh();

	def onLeaveUrl(self, event):
		event.GetEventObject().SetForegroundColour(self.__params["blurUrlColor"]);
		event.GetEventObject().Refresh();

	def onClickUrl(self, event):
		if wx.MessageDialog(self,"查看平台官网需要打开浏览器，是否确认打开？", "打开浏览器提示", style = wx.OK|wx.CANCEL|wx.ICON_QUESTION).ShowModal() == wx.ID_OK:
			self.getCtr().openUrl(event.GetEventObject().GetLabel());
		pass;

	def createAPPTitle(self):
		self.__appTitle = wx.StaticText(self, label = _GG("AppConfig")["AppTitle"], style = wx.ALIGN_CENTER);
		self.__appTitle.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));

	def createCopyrightInfo(self):
		self.__copyrightInfo = wx.StaticText(self, label = _GG("AppConfig")["CopyrightInfo"], style = wx.ALIGN_CENTER);
		self.__copyrightInfo.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
