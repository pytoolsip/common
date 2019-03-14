# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-01-26 18:49:31
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-14 21:22:33
import wx;
import math;

from _Global import _GG;
from function.base import *;

class RegisterDialogUI(wx.Dialog):
	"""docstring for RegisterDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(RegisterDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self.className_ = RegisterDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__inputInfosList = []; # 输入框列表
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
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

	def updateDialog(self, data):
		pass;

	def createInputViewsList(self):
		# 创建邮箱输入框
		emailParams = self.__params.get("email", {});
		def checkEmailInput(inputView, tipsView):
			label, color = "", "black";
			if not inputView.GetValue():
				self.updateTipsView(tipsView, "必须填写邮箱！", False);
			elif not self.getCtr().checkEmailFormat(inputView.GetValue()):
				self.updateTipsView(tipsView, "邮箱格式错误！", False);
			else:
				callback = emailParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateTipsView(tipsView, label, isOk);
					callback(inputView.GetValue(), update);
				else:
					self.updateTipsView(tipsView, "邮箱校验通过！");
		self.__email = self.createInfoInputPanel(params = {
			"size" : (self.GetSize().x, -1),
			"name" : emailParams.get("label", "邮箱"),
			"tips" : "*（必填）",
			"blurCallback" : checkEmailInput,
		});
		# 创建用户名输入框
		nameParams = self.__params.get("name", {});
		def checkNameInput(inputView, tipsView):
			label, color = "", "black";
			if not inputView.GetValue():
				self.updateTipsView(tipsView, "必须填写用户名！", False);
			elif not self.getCtr().checkNameFormat(inputView.GetValue()):
				self.updateTipsView(tipsView, "用户名格式错误！", False);
			else:
				callback = nameParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateTipsView(tipsView, label, isOk);
					callback(inputView.GetValue(), update);
				else:
					self.updateTipsView(tipsView, "用户名校验通过！");
		self.__name = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : nameParams.get("label", "用户名"),
			"tips" : "*（必填）",
			"blurCallback" : checkNameInput,
		});
		# 创建密码输入框
		def checkPwdInput(inputView, tipsView):
			label, color = "", "black";
			if not inputView.GetValue():
				self.updateTipsView(tipsView, "必须填写密码！", False);
			elif not self.getCtr().checkPwdFormat(inputView.GetValue()):
				self.updateTipsView(tipsView, "密码必须8-16位，且含数字和字母！", False);
			else:
				callback = nameParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateTipsView(tipsView, label, isOk);
					callback(inputView.GetValue(), update);
				else:
					self.updateTipsView(tipsView, "密码校验通过！");
		self.__pwd = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : "密码",
			"tips" : "*（必填）",
			"inputStyle" : wx.TE_PASSWORD,
			"blurCallback" : checkPwdInput,
		});
		# 创建确认密码输入框
		def checkConfirmPwdInput(inputView, tipsView):
			label, color = "", "black";
			if not inputView.GetValue():
				self.updateTipsView(tipsView, "必须填确认密码！", False);
			elif inputView.GetValue() == self.__pwd.input.GetValue():
				self.updateTipsView(tipsView, "确认密码校验通过！");
			else:
				self.updateTipsView(tipsView, "确认密码错误！", False);
		self.__confirmPwd = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : "确认密码",
			"tips" : "*（必填）",
			"inputStyle" : wx.TE_PASSWORD,
			"blurCallback" : checkConfirmPwdInput,
		});

	def createOKButton(self):
		self.__okButton = wx.Button(self, label = "确认注册", size = (-1, 30));
		self.__okButton.Bind(wx.EVT_BUTTON, self.onOkButton);

	def onOkButton(self, event):
		self.EndModal(wx.ID_OK);

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

	def updateTipsView(self, tipsView, label, isOk = True):
		color = isOk and "green" or "red";
		tipsView.SetLabel(label);
		tipsView.SetForegroundColour(color);

	def getRegisterInfo(self):
		return {
			"email" : self.__email.input.GetValue(),
			"name" : self.__name.input.GetValue(),
			"password" : self.__pwd.input.GetValue(),
		};