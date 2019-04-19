# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-03-26 18:25:37
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 00:23:01

import wx;

from _Global import _GG;
from function.base import *;

class ToolInfoDialogUI(wx.Dialog):
	"""docstring for ToolInfoDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(ToolInfoDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = ToolInfoDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "【%s】"%params.get("name", "标题"),
			"size" : (300,-1),
			"style" : wx.DEFAULT_DIALOG_STYLE,
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
		self.createName();
		self.createPath();
		self.createVersion();
		self.createAuthor();
		self.createDescription();
		self.createDownloadBtn();
		
	def initDialogLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__name, 0, flag = wx.TOP|wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.__path, 0, flag = wx.TOP|wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.__version, 0, flag = wx.TOP|wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.__author, 0, flag = wx.TOP|wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.__desc, 0, flag = wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.__download, 2, flag = wx.BOTTOM|wx.ALIGN_CENTER, border = 8);
		self.SetSizerAndFit(box);

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]));

	def updateDialog(self, data):
		pass;

	def resetDialog(self):
		pass;

	def createName(self):
		self.__name = wx.StaticText(self, label = self.__params.get("name", "工具名"));
		self.__name.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));

	def createPath(self):
		panel = wx.Panel(self);
		box = wx.BoxSizer(wx.HORIZONTAL);
		font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL);
		key = wx.StaticText(panel, label = "路径：");
		key.SetFont(font);
		panel._path = wx.StaticText(panel, label = self.__params.get("path", "--"));
		panel._path.SetFont(font);
		box.Add(key);
		box.Add(panel._path);
		panel.SetSizer(box);
		self.__path = panel;

	def createVersion(self):
		panel = wx.Panel(self);
		box = wx.BoxSizer(wx.HORIZONTAL);
		font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL);
		key = wx.StaticText(panel, label = "版本：");
		key.SetFont(font);
		panel._version = wx.StaticText(panel, label = self.__params.get("version", "-.-.-"));
		panel._version.SetFont(font);
		box.Add(key);
		box.Add(panel._version);
		panel.SetSizer(box);
		self.__version = panel;

	def createAuthor(self):
		panel = wx.Panel(self);
		box = wx.BoxSizer(wx.HORIZONTAL);
		font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL);
		key = wx.StaticText(panel, label = "作者：");
		key.SetFont(font);
		panel._name = wx.StaticText(panel, label = self.__params.get("author", "--"));
		panel._name.SetFont(font);
		box.Add(key);
		box.Add(panel._name);
		panel.SetSizer(box);
		self.__author = panel;

	def createDescription(self):
		params = self.__params.get("description", {});
		panel = wx.Panel(self);
		box = wx.BoxSizer(wx.HORIZONTAL);
		font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL);
		key = wx.StaticText(panel, label = "描述：");
		key.SetFont(font);
		panel._detail = wx.TextCtrl(panel, size = (self.GetSize()[0], params.get("height", 120)), value = params.get("value", ""), style = wx.TE_MULTILINE|wx.TE_READONLY);
		box.Add(key);
		box.Add(panel._detail, 0, flag = wx.EXPAND);
		panel.SetSizer(box);
		self.__desc = panel;

	def createDownloadBtn(self):
		params = self.__params.get("download", {});
		self.__download = wx.Button(self, label = params.get("label", "下载"));
		onDownload = params.get("onDownload", None);
		def onBtn(event):
			if callable(onDownload):
				onDownload();
			self.EndModal(wx.ID_OK);
		self.__download.Bind(wx.EVT_BUTTON, onBtn);
		if not onDownload:
			self.__download.Hide();
		elif not callable(onDownload):
			self.__download.Enable(False);