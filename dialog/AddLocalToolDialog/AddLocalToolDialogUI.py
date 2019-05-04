# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-04-05 22:36:48
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-13 20:12:35

import wx, math;

from _Global import _GG;
from function.base import *;
from ui import DirInputView;

class AddLocalToolDialogUI(wx.Dialog):
	"""docstring for AddLocalToolDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(AddLocalToolDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = AddLocalToolDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__inputInfosList = []; # 输入框列表
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "添加本地工具",
			"size" : (-1,-1),
			"style" : wx.DEFAULT_DIALOG_STYLE,
			"baseCategory" : "本地工具",
			"checkToolKey" : None,
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
		box.AddGrowableRow(len(self.__inputInfosList)/3);
		self.SetSizerAndFit(box);

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]));

	def updateDialog(self, data):
		if "name" in data:
			self.setInputPanelValue(self.__name, data["name"]);
		pass;

	def resetDialog(self):
		self.__dirInput.resetInputValue();
		self.updateInputPanel(self.__name, isReset = True);
		self.updateInputPanel(self.__category, label = self.getCategoryExTips(), isOk = True);
		self.updateInputPanel(self.__description, isReset = True);

	def createInputViewsList(self):
		self.createDirInputView();
		self.createCategoryView();
		self.createNameView();
		self.createDescriptionView();

	def createOKButton(self):
		self.__okButton = wx.Button(self, label = "确认添加", size = (-1, 30));
		def onOkButton(event):
			def onBtn(localToolInfo):
				callback = self.__params.get("onOk", None);
				if not callback or callback(localToolInfo):
					self.EndModal(wx.ID_OK);
				wx.MessageDialog(self, "添加本地工具【%s%s】成功。"%(localToolInfo["category"], localToolInfo["name"]), caption = "添加本地工具", style = wx.OK|wx.ICON_INFORMATION).ShowModal();
			self.getCtr().addLocalTool(self.getLocalToolInfo(), callback = onBtn);
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

	def setInputPanelValue(self, panel, value):
		panel.input.SetValue(value);
		if "blurCallback" in panel._params:
			panel._params["blurCallback"](panel);

	def createInputPanel(self, params):
		panel = wx.Panel(self);
		panel._params = params; # 保存params属性
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
		if self.checkInputView():
			self.__okButton.Enable();

	# 创建工具路径输入框
	def createDirInputView(self):
		params = self.__params.get("dirInput", {});
		name = wx.StaticText(self, label = params.get("name", "工具路径"));
		self.__dirInput = DirInputView(self, params = {"buttonLabel" : "选择目录", "buttonSize" : (60, 20)});
		self.__fileInput = wx.Button(self, -1, "选择zip包", size = (60, 20));
		def onClickBtn(event):
			filePath = wx.FileSelector("选择zip格式的工具包");
			if filePath != "":
				if os.path.splitext(filePath)[-1] == ".zip":
					self.__dirInput.setInputValue(filePath);
				else:
					wx.MessageDialog(self, "压缩包格式错误！", caption = "选择zip工具包", style = wx.OK|wx.ICON_ERROR).ShowModal();
		self.__fileInput.Bind(wx.EVT_BUTTON, onClickBtn);
		# 添加到信息列表中
		self.__inputInfosList.append((name, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((self.__dirInput, 0, wx.EXPAND|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((self.__fileInput, 0, wx.TOP|wx.LEFT|wx.RIGHT, 8));

	# 创建工具名输入框
	def createNameView(self):
		nameParams = self.__params.get("name", {});
		self.__name = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : nameParams.get("label", "工具名称"),
			"tips" : "*（必填）",
			"blurCallback" : self.checkNameInput,
		});

	def checkNameInput(self, panel = None):
		nameParams = self.__params.get("name", {});
		if not panel:
			panel = self.__name;
		if not panel.input.GetValue():
			self.updateInputPanel(panel, "必须填写工具名！", False);
		elif not self.getCtr().checkNameFormat(panel.input.GetValue()):
			self.updateInputPanel(panel, "工具名不能包含特殊字符！", False);
		else:
			fullName = self.getToolFullName(panel.input.GetValue());
			checkToolKey = self.__params.get("checkToolKey", None);
			if checkToolKey and not checkToolKey(self.getCtr().getKeyByName(fullName)):
				self.updateInputPanel(panel, "该分类下已存在相同工具名！", False);
			else:
				callback = nameParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateInputPanel(panel, label, isOk);
					callback(fullName, update);
				else:
					self.updateInputPanel(panel, "工具名校验通过！");

	def getCategoryExTips(self):
		return "注意：该分类位于【%s】类别下。"%self.__params["baseCategory"];

	def createCategoryView(self):
		categoryParams = self.__params.get("category", {});
		exTips = self.getCategoryExTips();
		def checkCategoryInput(panel):
			panel.input.SetValue(panel.input.GetValue().replace(" ", ""));
			if not panel.input.GetValue():
				self.updateInputPanel(panel, exTips);
			else:
				# 校验分类值
				panel.input.SetValue(self.getCtr().verifyCategory(panel.input.GetValue()));
				# 检测扩展分类
				ret, tips = self.getCtr().checkCategory(panel.input.GetValue());
				if not ret:
					self.updateInputPanel(panel, tips, False);
				else:
					callback = categoryParams.get("onBlur", None);
					if callback:
						def update(label, isOk = True):
							self.updateInputPanel(panel, label, isOk);
						callback(panel.input.GetValue(), update);
					else:
						self.updateInputPanel(panel, exTips);
			if panel.isOk:
				if self.__name.input.GetValue():
					self.checkNameInput();
		self.__category = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : categoryParams.get("label", "工具分类"),
			"tips" : "（请用/分割）",
			"exTips" : exTips,
			"blurCallback" : checkCategoryInput,
		});
		self.__category.isOk = True;

	def createDescriptionView(self):
		descriptionParams = self.__params.get("description", {});
		def checkDescriptionInput(panel):
			callback = descriptionParams.get("onBlur", None);
			if callback:
				def update(label, isOk = True):
					self.updateInputPanel(panel, label, isOk);
				callback(panel.input.GetValue(), update);
			else:
				self.updateInputPanel(panel, "");
		self.__description = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : descriptionParams.get("label", "工具简介"),
			"inputSize" : descriptionParams.get("inputSize", (-1, 100)),
			"inputStyle" : wx.TE_MULTILINE,
			"blurCallback" : checkDescriptionInput,
		});

	# 检测工具全称【包含分类路径】
	def getToolFullName(self, name):
		nameList = [self.__params["baseCategory"]];
		category = self.__category.input.GetValue();
		if category != "":
			nameList.append(self.getCtr().verifyBackslash(category));
		nameList.append(name);
		return "/".join(nameList);

	def checkInputView(self, key = "a"):
		if key in ["a", "dirInput"]:
			if not self.__dirInput.getInputValue():
				return False;
		if key in ["a", "name"]:
			if not self.__name.isOk:
				return False;
		if key in ["a", "category"]:
			if not self.__category.isOk:
				return False;
		return True;

	def getLocalToolInfo(self):
		fullName = self.getToolFullName(self.__name.input.GetValue());
		return {
			"filePath" : self.__dirInput.getInputValue(),
			"category" : self.getCtr().verifyBackslash(self.getToolFullName("")),
			"name" : self.__name.input.GetValue(),
			"description" : self.__description.input.GetValue(),
			"tkey" : self.getCtr().getKeyByName(fullName),
		};