# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-08-18 22:21:46
# @Last Modified by:   Administrator
# @Last Modified time: 2019-08-18 22:21:46

import wx;

from _Global import _GG;
from function.base import *;
from ui import DirInputView;

class PackDialogUI(wx.Dialog):
	"""docstring for PackDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(PackDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = PackDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "打包工具",
			"size" : (-1,-1),
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
		self.createTitleText();
		self.createDirInputView();
		self.createZipButton();
		self.createTipsText();
		pass;
		
	def initDialogLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.__title, 0, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		box.Add(self.__dirInput, 0, flag = wx.TOP|wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.__tips, 0, flag = wx.TOP|wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.__zipButton, 0, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 10);
		self.SetSizerAndFit(box);
		pass;

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]/2));

	def updateDialog(self, data):
		pass;

	def resetDialog(self):
		self.__dirInput.resetInputValue();
		self.showTips("");
		pass;

	def createTitleText(self):
		self.__title = wx.StaticText(self, label = "-选择打包路径-");
		self.__title.SetForegroundColour("gray");
		self.__title.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));

	# 创建工具路径输入框
	def createDirInputView(self):
		self.__dirInput = DirInputView(self, params = {"inputSize" : (200, 20), "buttonLabel" : "选择目录", "buttonSize" : (60, 20)});

	def createZipButton(self):
		self.__zipButton = wx.Button(self, label = "点击打包(zip)", size = (-1, 30));
		def onOkButton(event):
			if self.getCtr().onPackPath(self.__dirInput.getInputValue()):
				self.EndModal(wx.ID_OK);
		self.__zipButton.Bind(wx.EVT_BUTTON, onOkButton);

	def createTipsText(self):
		self.__tips = wx.StaticText(self, label = "");
		self.__tips.SetForegroundColour("red");
		self.__tips.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		self.showTips("");

	def showTips(self, tips):
		self.__tips.SetLabel(tips);
