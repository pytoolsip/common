# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-16 03:04:58
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-18 22:30:08
import wx, math;

from _Global import _GG;
from function.base import *;
from ui import DirInputView;

class UploadDialogUI(wx.Dialog):
	"""docstring for UploadDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(UploadDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = UploadDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__inputInfosList = []; # 输入框列表
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/UpDownloadBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "标题",
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

	def resetDialog(self):
		self.__dirInput.resetInputValue();
		self.updateInputPanel(self.__name, isReset = True);
		self.updateOnlineVersionView("无");
		self.updateInputPanel(self.__version, isReset = True);
		self.__commonVersion.SetLabel(_GG("AppConfig")["version"]);
		self.updateInputPanel(self.__description, isReset = True);

	def createInputViewsList(self):
		self.createDirInputView();
		self.createNameView();
		self.createOnlineVersionView();
		self.createVersionView();
		self.createConmonVersionView();
		self.createDescriptionView();

	def createOKButton(self):
		self.__okButton = wx.Button(self, label = "确认上传", size = (-1, 30));
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
		if self.checkInputView():
			self.__okButton.Enable();

	# 创建工具路径输入框
	def createDirInputView(self):
		params = self.__params.get("dirInput", {});
		name = wx.StaticText(self, label = params.get("name", "工具路径"));
		self.__dirInput = DirInputView(self, params = {"buttonLabel" : "选择目录", "buttonSize" : (60, 20), "onInput" : self.onInputToolFile});
		self.__dirInput.isOk = False;
		self.__fileInput = wx.Button(self, -1, "选择zip包", size = (60, 20));
		def onClickBtn(event):
			filePath = wx.DirSelector();
			if filePath != "":
				if os.path.splitext(filePath)[-1] == ".zip":
					self.__dirInput.setInputValue(filePath);
				else:
					wx.MessageDialog(self, "压缩包格式错误！", caption = "选择zip工具包", style = wx.OK|wx.ICON_ERROR).ShowModal();
		self.__fileInput.Bind(wx.EVT_BUTTON, onClickBtn);
		# 添加到信息列表中
		self.__inputInfosList.append((name, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((self.__dirInput, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((self.__fileInput, 0, wx.TOP|wx.LEFT|wx.RIGHT, 8));

	# 创建工具名输入框
	def createNameView(self):
		nameParams = self.__params.get("name", {});
		def checkNameInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写工具名！", False);
			elif not self.getCtr().checkNameFormat(panel.input.GetValue()):
				self.updateInputPanel(panel, "工具名格式错误！", False);
			else:
				callback = nameParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateInputPanel(panel, label, isOk);
					callback(panel.input.GetValue(), update);
				else:
					self.updateInputPanel(panel, "工具名校验通过！");
		self.__name = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : nameParams.get("label", "工具名"),
			"tips" : "*（必填）",
			"blurCallback" : checkNameInput,
		});

	# 创建线上版本视图
	def createOnlineVersionView(self):
		params = self.__params.get("onlineVersion", {});
		name = wx.StaticText(self, label = params.get("name", "线上版本"));
		self.__onlineVersion = wx.StaticText(self, label = "无");
		# 添加到信息列表中
		self.__inputInfosList.append((name, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((self.__onlineVersion, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((wx.Panel(self)));

	# 更新线上版本视图
	def updateOnlineVersionView(self, version):
		self.__onlineVersion.SetLabel(version);

	def createVersionView(self):
		versionParams = self.__params.get("version", {});
		def checkVersionInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写版本！", False);
			elif not self.getCtr().checkVersion(panel.input.GetValue(), self.__onlineVersion.GetLabel()):
				self.updateInputPanel(panel, "版本填写错误！", False);
			else:
				callback = versionParams.get("onBlur", None);
				if callback:
					def update(label, isOk = True):
						self.updateInputPanel(panel, label, isOk);
					callback(panel.input.GetValue(), update);
				else:
					self.updateInputPanel(panel, "版本校验通过！");
		self.__version = self.createInfoInputPanel(params = {
			"size" : (-1, -1),
			"name" : versionParams.get("label", "版本"),
			"tips" : "*（必填）",
			"blurCallback" : checkVersionInput,
		});

	def createConmonVersionView(self):
		params = self.__params.get("conmonVersion", {});
		name = wx.StaticText(self, label = params.get("name", "IP版本"));
		self.__commonVersion = wx.StaticText(self, label = _GG("AppConfig")["version"]);
		# 添加到信息列表中
		self.__inputInfosList.append((name, 0, wx.ALIGN_RIGHT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((self.__commonVersion, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT, 8));
		self.__inputInfosList.append((wx.Panel(self)));

	def createDescriptionView(self):
		descriptionParams = self.__params.get("description", {});
		def checkDescriptionInput(panel):
			if not panel.input.GetValue():
				self.updateInputPanel(panel, "必须填写工具简介！", False);
			else:
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
			"tips" : "*（必填）",
			"blurCallback" : checkDescriptionInput,
		});

	def onInputToolFile(self, filePath, callback):
		if filePath != "" and os.path.exists(filePath):
			if os.path.isdir(filePath):
				fileName = os.path.basename(filePath);
				if not os.path.exists(_GG("g_DataPath")+"temp/zip"):
					os.mkdir(_GG("g_DataPath")+"temp/zip");
				zipFilePath = _GG("g_DataPath") + "temp/zip/" + "%s_%d.zip"%(fileName, int(time.time()));
				self.zipFile(filePath, zipFilePath); # 压缩filePath为zip包
				filePath = zipFilePath; # 重置filePath
			if os.path.splitext(filePath)[-1] == ".zip":
				pass;
		return callback(zipFilePath);

	def checkInputView(self, key = "a"):
		if key in ["a", "dirInput"]:
			if not self.__dirInput.isOk:
				return False;
		elif key in ["a", "name"]:
			if not self.__name.isOk:
				return False;
		elif key in ["a", "version"]:
			if not self.__version.isOk:
				return False;
		elif key in ["a", "description"]:
			if not self.__description.isOk:
				return False;
		return True;