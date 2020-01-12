# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2020-01-12 13:31:23
# @Last Modified by:   Administrator
# @Last Modified time: 2020-01-12 13:31:23

import wx;
import math;

from _Global import _GG;
from function.base import *;
from ui import DirInputView;

class CreateTemplateDialogUI(wx.Dialog):
	"""docstring for CreateTemplateDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(CreateTemplateDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = CreateTemplateDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件
		self.__viewList = [];

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "新建模板",
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
		self.onModuleCombobox();

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***Dialog"); # , parent = self, params = {}
		self.createModuleComboBox();
		self.createDirInput();
		self.createTargetName();
		self.createOkBtn();
		pass;
		
	def initDialogLayout(self):
		flexGridSizer = wx.FlexGridSizer(math.ceil(len(self.__viewList)/2), 2, 2, 2);
		flexGridSizer.AddMany(self.__viewList);
		flexGridSizer.AddGrowableCol(0, 1);
		self.SetSizerAndFit(flexGridSizer);
		pass;

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]/2));

	def updateDialog(self, data):
		pass;

	def resetDialog(self):
		pass;

	def createModuleComboBox(self):
		title = wx.StaticText(self, label = "选择模板：");
		title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		modList = self.getCtr().getModuleList();
		default = len(modList) > 0 and modList[0] or "";
		self.__modCbb = wx.ComboBox(self, value = default, choices = modList, style = wx.CB_READONLY);
		self.__modCbb.Bind(wx.EVT_COMBOBOX, self.onModuleCombobox);
		# 添加到视图列表中
		self.__viewList.append((title, -1, wx.ALIGN_CENTER|wx.TOP|wx.LEFT, 20));
		self.__viewList.append((self.__modCbb, -1, wx.TOP|wx.RIGHT|wx.EXPAND, 20));
	
	def onModuleCombobox(self, event = None):
		mod = self.__modCbb.GetValue();
		self.__targetName.SetValue("Template" + mod.capitalize());
		pass;

	def createDirInput(self):
		title = wx.StaticText(self, label = "选择生成目录：");
		title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		self.__dirInput = DirInputView(self, params = {"inputSize" : (200, 20), "buttonLabel" : "选择目录", "buttonSize" : (60, 20)});
		# 添加到视图列表中
		self.__viewList.append((title, -1, wx.ALIGN_CENTER|wx.TOP|wx.LEFT, 20));
		self.__viewList.append((self.__dirInput, -1, wx.TOP|wx.RIGHT, 20));
	
	def createTargetName(self):
		title = wx.StaticText(self, label = "生成名称：");
		title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		self.__targetName = wx.TextCtrl(self, -1, "", size = (100, -1));
		# 添加到视图列表中
		self.__viewList.append((title, -1, wx.ALIGN_CENTER|wx.TOP|wx.LEFT, 20));
		self.__viewList.append((self.__targetName, -1, wx.TOP|wx.RIGHT|wx.EXPAND, 20));

	def createOkBtn(self):
		self.__okBtn = wx.Button(self, label = "确认生成", size = (80, 28));
		self.__okBtn.Bind(wx.EVT_BUTTON, self.onOkButton);
		# 添加到视图列表中
		self.__viewList.append((wx.Panel(self), -1, wx.TOP|wx.BOTTOM|wx.LEFT, 20));
		self.__viewList.append((self.__okBtn, -1, wx.TOP|wx.BOTTOM|wx.RIGHT, 20));

	def onOkButton(self, event):
		modName, targetModName, targetModPath = self.__modCbb.GetValue(), self.__targetName.GetValue(), self.__dirInput.getInputValue();
		if not modName:
			self.showMsgDialog("所选模板不存在！", style = wx.OK|wx.ICON_ERROR);
			return;
		if not targetModName:
			self.showMsgDialog("生成名称不能为空！", style = wx.OK|wx.ICON_ERROR);
			return;
		if not targetModPath:
			self.showMsgDialog("生成目录不能为空！", style = wx.OK|wx.ICON_ERROR);
			return;
		# 创建模板
		targetPath = targetModPath;
		try:
			ret, targetPath = self.getCtr().createMod(modName, targetModName, targetModPath);
			if not ret:
				if targetPath == "invalid":
					self.showMsgDialog(f"无效模板【{modName}】，生成失败！", style = wx.OK|wx.ICON_ERROR);
				elif targetPath == "existed":
					self.showMsgDialog("该目录下已存在相同名称的模板，生成失败！", style = wx.OK|wx.ICON_ERROR);
				else:
					self.showMsgDialog("生成模板失败，请重试！", style = wx.OK|wx.ICON_ERROR);
				return;
		except Exception as e:
			_GG("Log").w("Create Template Error!", e);
			self.showMsgDialog("生成模板失败，请重试！", style = wx.OK|wx.ICON_ERROR);
			return;
		# 创建成功回调
		callback = self.__params.get("onOk", None);
		if callable(callback):
			callback(targetPath);
		# 关闭弹窗
		self.EndModal(wx.ID_OK);

	def showMsgDialog(self, *argList, caption = "新建模板", **argDict):
		return wx.MessageDialog(self, *argList, caption = caption, **argDict).ShowModal();