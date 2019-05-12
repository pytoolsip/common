# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-28 14:23:53
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-23 17:12:04

import wx;
import math;

from _Global import _GG;
from function.base import *;

class LoginDialogUI(wx.Dialog):
	"""docstring for LoginDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(LoginDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = LoginDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__inputInfosList = []; # 输入框列表
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "用户登录",
			"size" : (-1,-1),
			"style" : wx.DEFAULT_DIALOG_STYLE,
			"name" : {
				"label" : "用户名",
				# "onInput" : None,
				"onBlur" : None,
			},
			"password" : {
				"label" : "密码",
				# "onInput" : None,
				"onBlur" : None,
			},
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
		self.createInputViewsList();
		self.createOKButton();
		
	def initDialogLayout(self):
		box = wx.FlexGridSizer(3, math.ceil(len(self.__inputInfosList)/3), 4);
		box.AddMany(self.__inputInfosList);
		box.Add(wx.Panel(self));
		box.Add(self.__okButton, flag = wx.ALIGN_RIGHT|wx.BOTTOM, border = 10);
		self.SetSizerAndFit(box);

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]/2));

	def updateDialog(self, data):
		pass;

	def resetDialog(self):
		self.updateInputPanel(self.__name, isReset = True);
		self.updateInputPanel(self.__pwd, isReset = True);
		pass;

	def createInputViewsList(self):
		# 创建用户名输入框
		nameParams = self.__params.get("name", {});
		def checkNameInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写用户名！", False);
			else:
				callback = nameParams.get("onBlur", None);
				if callback:
					callback(panel.input.GetValue(), self.updateNameInput);
				else:
					self.updateInputPanel(panel, "");
		self.__name = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : nameParams.get("label", "用户名"),
			"blurCallback" : checkNameInput,
		});
		# 创建密码输入框
		pwdParams = self.__params.get("password", {});
		def checkPwdInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写密码！", False);
			else:
				callback = pwdParams.get("onBlur", None);
				if callback:
					callback(panel.input.GetValue(), self.updatePwdInput);
				else:
					self.updateInputPanel(panel, "");
		self.__pwd = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : pwdParams.get("label", "密码"),
			"inputStyle" : wx.TE_PASSWORD,
			"blurCallback" : checkPwdInput,
		});

	def createOKButton(self):
		self.__okButton = wx.Button(self, label = "确认登录", size = (-1, 30));
		def onOkButton(event):
			callback = self.__params.get("onOk", None);
			if callback:
				if callback(self.getLoginInfo()):
					self.EndModal(wx.ID_OK);
			else:
				self.EndModal(wx.ID_OK);
		self.__okButton.Bind(wx.EVT_BUTTON, onOkButton);
		self.__okButton.Enable(False);

	def createInfoInputPanel(self, params = {}):
		name = wx.StaticText(self, label = params.get("name", ""));
		self.__inputInfosList.append((name, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		inputPanel = self.createInputPanel(params);
		self.__inputInfosList.append((inputPanel, 1, wx.EXPAND|wx.TOP|wx.LEFT, 8));
		tips = wx.StaticText(self, label = params.get("tips", ""));
		self.__inputInfosList.append((tips, 0, wx.TOP|wx.LEFT, 8));
		return inputPanel;

	def createInputPanel(self, params):
		panel = wx.Panel(self);
		panel.input = wx.TextCtrl(panel, -1, "", size = params.get("inputSize", (-1,20)), style = params.get("inputStyle", wx.TE_PROCESS_TAB));
		panel.tips = wx.StaticText(panel, label = params.get("exTips", ""));
		panel.tips.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		if params.get("isHideExTips", False):
			wx.CallAfter(panel.tips.Hide);
		# 绑定事件
		if "inputCallback" in params:
			def onInput(event):
				params.get("inputCallback")(panel);
			panel.input.Bind(wx.EVT_TEXT, onInput);
		if "blurCallback" in params:
			def onBlur(event):
				params.get("blurCallback")(panel);
				event.Skip();
			panel.input.Bind(wx.EVT_KILL_FOCUS, onBlur);
		# 布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(panel.input, 1, flag = wx.EXPAND);
		box.Add(panel.tips, 0, flag = wx.TOP, border = 1);
		panel.SetSizer(box);
		# 初始化输入校验结果
		panel.isOk = False;
		return panel;

	def updateInputPanel(self, panel, label = "", isOk = True, isReset = False):
		color = isOk and "black" or "red";
		if isReset == True:
			label, isOk, color = "", False, "black";
		# 更新属性
		panel.isOk = isOk;
		panel.tips.SetLabel(label);
		panel.tips.SetForegroundColour(color);
		# 检测输入框，并设置相应按钮的可点击逻辑
		if self.checkInputView():
			self.__okButton.Enable();

	def checkInputView(self, key = "a"):
		if key in ["a", "name"]:
			if not self.__name.isOk:
				return False;
		if key in ["a", "pwd"]:
			if not self.__pwd.isOk:
				return False;
		return True;

	def getLoginInfo(self):
		return {
			"name" : self.__name.input.GetValue(),
			"password" : self.__pwd.input.GetValue(),
		};