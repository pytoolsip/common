# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-13 23:07:38
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 19:00:01

import wx;

from _Global import _GG;
from function.base import *;

class AboutIPDialogUI(wx.Dialog):
	"""docstring for AboutIPDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(AboutIPDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self.className_ = AboutIPDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "关于",
			"size" : (-1,-1),
			"style" : wx.DEFAULT_DIALOG_STYLE,
			"focusUrlColor" : wx.Colour(0,128,255),
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
		self.createVersionTitle();
		self.createVersionValue();
		self.createWebsiteTitle();
		self.createWebsiteUrl();
		
	def initDialogLayout(self):
		# 创建flexGridSizer，并设置相应控件和参数
		flexGridSizer = wx.FlexGridSizer(2, 2, 2, 2);
		flexGridSizer.AddMany([
			(self.versionTitle, -1, wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, 10),
			(self.versionValue, -1, wx.TOP|wx.BOTTOM|wx.RIGHT, 10),
			(self.websiteTitle, -1, wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, 10),
			(self.websiteUrl, -1, wx.TOP|wx.BOTTOM|wx.RIGHT, 10)
		]);
		flexGridSizer.AddGrowableCol(0, 1);
		self.SetSizerAndFit(flexGridSizer);

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]));

	def updateDialog(self, data):
		pass;

	def createVersionTitle(self):
		self.versionTitle = wx.StaticText(self, label = "版本号：");
		self.versionTitle.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));

	def createVersionValue(self):
		self.versionValue = wx.StaticText(self, label = _GG("AppConfig")["version"]);
		self.versionValue.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		self.versionValue.SetForegroundColour(wx.Colour(0,100,0));

	def createWebsiteTitle(self):
		self.websiteTitle = wx.StaticText(self, label = "官网：");
		self.websiteTitle.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));

	def createWebsiteUrl(self):
		# self.websiteUrl = wx.TextCtrl(self, value = "https://legacy.gitbook.com/book/jimdreamheart/jimsbook", style = wx.TE_AUTO_URL);
		self.websiteUrl = wx.StaticText(self, label = "https://legacy.gitbook.com/book/jimdreamheart/jimsbook");
		self.websiteUrl.SetForegroundColour("blue");
		self.websiteUrl.Bind(wx.EVT_ENTER_WINDOW, self.onEnterUrl);
		self.websiteUrl.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaveUrl);
		self.websiteUrl.Bind(wx.EVT_LEFT_DOWN, self.onClickUrl);

	def onEnterUrl(self, event):
		event.GetEventObject().SetForegroundColour(self.__params["focusUrlColor"]);
		event.GetEventObject().Refresh();

	def onLeaveUrl(self, event):
		event.GetEventObject().SetForegroundColour("blue");
		event.GetEventObject().Refresh();

	def onClickUrl(self, event):
		self.getCtr().openUrl(event.GetEventObject().GetLabel());