# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-01-26 18:49:31
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-19 23:56:34
import wx;
import math;

from _Global import _GG;
from function.base import *;

class RegisterDialogUI(wx.Dialog):
	"""docstring for RegisterDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(RegisterDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = RegisterDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__inputInfosList = []; # 输入框列表
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件
		self.createTimer(); # 创建校验验证码定时器

	def __del__(self):
		self.stopTimer(True);

	def onClose(self, event):
		self.stopTimer();
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "用户注册",
			"size" : (-1,-1),
			"style" : wx.DEFAULT_DIALOG_STYLE,
			"name" : {
				"label" : "用户名",
				# "onInput" : None,
				"onBlur" : None,
			},
			"email" : {
				"label" : "邮箱",
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
		box = wx.FlexGridSizer(3, math.ceil(len(self.__inputInfosList)/3), 2);
		box.AddMany(self.__inputInfosList);
		box.Add(wx.Panel(self));
		box.Add(self.__okButton, flag = wx.ALIGN_CENTER|wx.BOTTOM, border = 10);
		self.SetSizerAndFit(box);

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]));

	def createTimer(self):
		self.__timer = _GG("TimerManager").createTimer(self, callback = self.onTimerEvent);

	def startTimer(self, callback):
		if self.__timer.IsRunning():
			self.__timer.Stop();
		self.__timer.Start(1000);
		self.__timerCallback = callback;

	def stopTimer(self, isDestroy = False):
		if self.__timer.IsRunning():
			self.__timer.Stop();
		if isDestroy:
			_GG("TimerManager").deleteTimer(self.__timer);

	def onTimerEvent(self, event):
		if hasattr(self, "__timerCallback"):
			self.__timerCallback();

	def updateDialog(self, data):
		pass;

	def resetDialog(self):
		self.updateInputPanel(self.__email, isReset = True);
		self.updateInputPanel(self.__veriCode, isReset = True);
		self.updateInputPanel(self.__name, isReset = True);
		self.updateInputPanel(self.__pwd, isReset = True);
		self.updateInputPanel(self.__confirmPwd, isReset = True);
		pass;

	def createInputViewsList(self):
		self.createEmailView();
		self.createVerificationCodeView();
		self.createNameView();
		self.createPwdView();
		self.createConfirmPwdView();

	# 创建邮箱输入框
	def createEmailView(self):
		emailParams = self.__params.get("email", {});
		def checkEmailInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写邮箱！", False);
			elif not self.getCtr().checkEmailFormat(panel.input.GetValue()):
				self.updateInputPanel(panel, "邮箱格式错误！", False);
			else:
				callback = emailParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateInputPanel(panel, label, isOk);
					callback(panel.input.GetValue(), update);
				else:
					self.updateInputPanel(panel, "邮箱校验通过！");
		self.__email = self.createInfoInputPanel(params = {
			"size" : (self.GetSize().x, -1),
			"name" : emailParams.get("label", "邮箱"),
			"tips" : "*（必填）",
			"blurCallback" : checkEmailInput,
		});

	# 创建用户名输入框
	def createNameView(self):
		nameParams = self.__params.get("name", {});
		def checkNameInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写用户名！", False);
			elif not self.getCtr().checkNameFormat(panel.input.GetValue()):
				self.updateInputPanel(panel, "用户名不能包含特殊字符！", False);
			else:
				callback = nameParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateInputPanel(panel, label, isOk);
					callback(panel.input.GetValue(), update);
				else:
					self.updateInputPanel(panel, "用户名校验通过！");
		self.__name = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : nameParams.get("label", "用户名"),
			"tips" : "*（必填）",
			"blurCallback" : checkNameInput,
		});

	# 创建密码输入框
	def createPwdView(self):
		pwdParams = self.__params.get("password", {});
		def checkPwdInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写密码！", False);
			elif not self.getCtr().checkPwdFormat(panel.input.GetValue()):
				self.updateInputPanel(panel, "密码必须8-16位，且含数字和字母！", False);
			else:
				callback = pwdParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateInputPanel(panel, label, isOk);
					callback(panel.input.GetValue(), update);
				else:
					self.updateInputPanel(panel, "密码校验通过！");
		self.__pwd = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : "密码",
			"tips" : "*（必填）",
			"inputStyle" : wx.TE_PASSWORD,
			"blurCallback" : checkPwdInput,
		});

	# 创建确认密码输入框
	def createConfirmPwdView(self):
		def checkConfirmPwdInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填确认密码！", False);
			elif panel.input.GetValue() == self.__pwd.input.GetValue():
				self.updateInputPanel(panel, "确认密码校验通过！");
			else:
				self.updateInputPanel(panel, "确认密码错误！", False);
		self.__confirmPwd = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : "确认密码",
			"tips" : "*（必填）",
			"inputStyle" : wx.TE_PASSWORD,
			"blurCallback" : checkConfirmPwdInput,
		});

	# 创建验证码输入框
	def createVerificationCodeView(self):
		veriCodeParams = self.__params.get("veriCode", {});
		def checkCodeInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写验证码！", False);
			else:
				callback = veriCodeParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateInputPanel(panel, label, isOk);
					callback(self.__email.input.GetValue(), panel.input.GetValue(), update);
				else:
					self.updateInputPanel(panel, "验证码校验通过！");
		self.__veriCode = self.createInputPanel({
			"inputStyle" : wx.TE_PASSWORD,
			"blurCallback" : checkCodeInput,
		});
		self.__veriCodeBtn = wx.Button(self, label = "发送验证码", size = (-1, 21));
		def onVeriCodeBtn(event):
			callback = veriCodeParams.get("onBtn", None);
			if callback:
				def onCallback(expire):
					self.__veriCodeBtn.SetLabel(str(expire)+"s");
					def onTimer():
						expire -= 1;
						self.__veriCodeBtn.SetLabel(str(expire)+"s");
						if expire == 0:
							self.__veriCodeBtn.SetLabel("发送验证码");
							self.__veriCodeBtn.Enable();
							self.stopTimer();
					self.startTimer(onTimer);
				callback(self.__email.input.GetValue(), onCallback);
			self.__veriCodeBtn.SetLabel("已发送");
			self.__veriCodeBtn.Enable(False);
		self.__veriCodeBtn.Bind(wx.EVT_BUTTON, onVeriCodeBtn);
		self.__veriCodeBtn.Enable(False);
		# 添加到输入信息列表
		name = wx.StaticText(self, label = veriCodeParams.get("name", "邮箱验证"));
		self.__inputInfosList.append((name, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((self.__veriCode, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((self.__veriCodeBtn, 2, wx.ALIGN_LEFT|wx.TOP, 8));

	def createOKButton(self):
		self.__okButton = wx.Button(self, label = "确认注册", size = (-1, 30));
		def onOkButton(event):
			callback = self.__params.get("onOk", None);
			if callback:
				if callback(self.getRegisterInfo()):
					self.EndModal(wx.ID_OK);
			else:
				self.EndModal(wx.ID_OK);
		self.__okButton.Bind(wx.EVT_BUTTON, onOkButton);
		self.__okButton.Enable(False);

	def createInfoInputPanel(self, params = {}):
		name = wx.StaticText(self, label = params.get("name", "名称"));
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
		color = isOk and "green" or "red";
		if isReset == True:
			label, isOk, color = "", False, "green";
		# 更新属性
		panel.isOk = isOk;
		panel.tips.SetLabel(label);
		panel.tips.SetForegroundColour(color);
		# 检测输入框，并设置相应按钮的可点击逻辑
		if self.checkInputView("email"):
			self.__veriCodeBtn.Enable();
		if self.checkInputView():
			self.__okButton.Enable();

	def checkInputView(self, key = "a"):
		if key in ["a", "email"]:
			if not self.__email.isOk:
				return False;
		elif key in ["a", "name"]:
			if not self.__name.isOk:
				return False;
		elif key in ["a", "pwd"]:
			if not self.__pwd.isOk:
				return False;
		elif key in ["a", "confirmPwd"]:
			if not self.__confirmPwd.isOk:
				return False;
		elif key in ["a", "veriCode"]:
			if not self.__veriCode.isOk:
				return False;
		return True;

	def getRegisterInfo(self):
		return {
			"email" : self.__email.input.GetValue(),
			"name" : self.__name.input.GetValue(),
			"password" : self.__pwd.input.GetValue(),
			"veriCode" : self.__veriCode.input.GetValue(),
		};