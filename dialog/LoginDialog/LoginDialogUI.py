# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-01-28 14:23:53
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 19:00:04

import wx;
import math;

from _Global import _GG;
from function.base import *;

class LoginDialogUI(wx.Dialog):
	"""docstring for LoginDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(LoginDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self.className_ = LoginDialogUI.__name__;
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
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]));

	def updateDialog(self, data):
		pass;

	def resetView(self):
		self.updateNameInput("", "black");
		self.updatePwdInput("", "black");
		pass;

	def createInputViewsList(self):
		# 创建用户名输入框
		nameParams = self.__params.get("name", {});
		def checkNameInput(inputView, tipsView):
			label, color = "", "black";
			if not inputView.GetValue():
				self.updateNameInput("必须填写用户名！", "red");
			else:
				callback = nameParams.get("onBlur", None);
				if callback:
					callback(inputView.GetValue(), self.updateNameInput);
				else:
					self.updateNameInput("", "black");
		self.__name = self.createInfoInputView(params = {
			"size" : (-1, -1),
			"name" : nameParams.get("label", "用户名"),
			"blurCallback" : checkNameInput,
		});
		# 创建密码输入框
		pwdParams = self.__params.get("password", {});
		def checkPwdInput(inputView, tipsView):
			label, color = "", "black";
			if not inputView.GetValue():
				self.updatePwdInput("必须填写密码！", "red");
			else:
				callback = pwdParams.get("onBlur", None);
				if callback:
					callback(inputView.GetValue(), self.updatePwdInput);
				else:
					self.updatePwdInput("", "black");
			tipsView.SetLabel(label);
			tipsView.SetForegroundColour(color);
		self.__pwd = self.createInfoInputView(params = {
			"size" : (-1, -1),
			"name" : pwdParams.get("label", "密码"),
			"inputStyle" : wx.TE_PASSWORD,
			"blurCallback" : checkPwdInput,
		});

	def createOKButton(self):
		self.__okButton = wx.Button(self, label = "确认登录", size = (-1, 30));
		self.__okButton.Bind(wx.EVT_BUTTON, self.onOkButton);

	def onOkButton(self, event):
		self.EndModal(wx.ID_OK);

	def createInfoInputView(self, params = {}):
		name = wx.StaticText(self, label = params.get("name", ""));
		self.__inputInfosList.append((name, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		inputView = self.createInputView(params);
		self.__inputInfosList.append((inputView, 1, wx.EXPAND|wx.TOP|wx.LEFT, 8));
		tips = wx.StaticText(self, label = params.get("tips", ""));
		self.__inputInfosList.append((tips, 0, wx.TOP|wx.LEFT, 8));
		return inputView;

	def createInputView(self, params):
		panel = wx.Panel(self);
		inputView = wx.TextCtrl(panel, -1, "", size = params.get("inputSize", (-1,20)), style = params.get("inputStyle", wx.TE_PROCESS_TAB));
		tipsText = wx.StaticText(panel, label = params.get("exTips", ""));
		tipsText.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		if params.get("isHideExTips", False):
			wx.CallAfter(tipsText.Hide);
		# 绑定事件
		if "inputCallback" in params:
			def onInput(event):
				params.get("inputCallback")(inputView, tipsText);
			inputView.Bind(wx.EVT_TEXT, onInput);
		if "blurCallback" in params:
			def onBlur(event):
				params.get("blurCallback")(inputView, tipsText);
				event.Skip();
			inputView.Bind(wx.EVT_KILL_FOCUS, onBlur);
		# 布局
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(inputView, 1, flag = wx.EXPAND);
		box.Add(tipsText, 0, flag = wx.TOP, border = 1);
		panel.SetSizer(box);
		# 保存索引对象
		panel.input = inputView;
		panel.tips = tipsText;
		return panel;

	def updateNameInput(self, label, color):
		self.__name.tips.SetLabel(label);
		self.__name.tips.SetForegroundColour(color);

	def updatePwdInput(self, label, color):
		self.__pwd.tips.SetLabel(label);
		self.__pwd.tips.SetForegroundColour(color);

	def getLoginInfo(self):
		return {
			"name" : self.__name.input.GetValue(),
			"password" : self.__pwd.input.GetValue(),
		};