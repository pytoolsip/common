# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-27 15:28:41
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:47

import wx;

from _Global import _GG;
from function.base import *;
from ui import DirInputView;

class ToolDevelopInfoDialogUI(wx.Dialog):
	"""docstring for ToolDevelopInfoDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(ToolDevelopInfoDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"]);
		self._className_ = ToolDevelopInfoDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "工具开发",
			"size" : (300, 200),
			"name" : "工具名称",
			"dirName" : "工程路径",
			"textCtrlSize" : (-1, 20),
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
		self.createNames();
		self.createTextCtrl();
		self.createDirInput();
		self.createOKButton();
		
	def initDialogLayout(self):
		# 创建flexGridSizer，并设置相应控件和参数
		self.flexGridSizer = wx.FlexGridSizer(2, 2, 2, 4);
		self.flexGridSizer.AddMany([
			(self.name, -1, wx.EXPAND|wx.TOP|wx.BOTTOM, 6),
			(self.textCtrl, -1, wx.EXPAND|wx.TOP|wx.BOTTOM, 6),
			(self.dirName, -1, wx.EXPAND|wx.TOP|wx.BOTTOM, 6),
			(self.dirInput, -1, wx.EXPAND|wx.TOP|wx.BOTTOM, 6)
		]);
		self.flexGridSizer.AddGrowableCol(0, 1);
		# 将整个flexGridSizer扩充到整个左边的窗口
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.flexGridSizer, proportion = 2, flag = wx.ALL|wx.EXPAND, border = 8);
		box.Add(self.okButton, proportion = 0, flag = wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM, border = 4);
		self.SetSizerAndFit(box);

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]/2));

	def updateDialog(self, data):
		pass;

	def resetDialog(self):
		self.textCtrl.SetValue("");
		self.dirInput.resetInputValue();

	def createNames(self):
		self.name = wx.StaticText(self, label = self.__params["name"]);
		self.dirName = wx.StaticText(self, label = self.__params["dirName"]);

	def createTextCtrl(self):
		self.textCtrl = wx.TextCtrl(self, -1, "", size = self.__params["textCtrlSize"]);

	def createDirInput(self):
		self.dirInput = DirInputView(self);

	def getTextCtrlValue(self):
		return self.textCtrl.GetValue();

	def getDirInputValue(self):
		return self.dirInput.getInputValue();

	def createOKButton(self):
		self.okButton = wx.Button(self, label = "创建工具模板", size = (-1, 30));
		self.okButton.Bind(wx.EVT_BUTTON, self.onOkButton);

	def onOkButton(self, event):
		self.EndModal(wx.ID_OK);