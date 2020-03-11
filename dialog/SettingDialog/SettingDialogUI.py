# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2020-01-11 17:27:27
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-07 00:17:12

import wx;

from _Global import _GG;
from function.base import *;

class SettingDialogUI(wx.Dialog):
	"""docstring for SettingDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(SettingDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = SettingDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "平台设置",
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
		self.createPipInstallImage();
		self.createPageCountLimit();
		self.createSaveBtn();
		pass;
		
	def initDialogLayout(self):
		flexGridSizer = wx.FlexGridSizer(4, 2, 2, 2);
		flexGridSizer.AddMany([
			(self.piiTitle, -1, wx.ALIGN_CENTER|wx.TOP|wx.LEFT, 20),
			(self.piiValue, -1, wx.TOP|wx.RIGHT, 20),
			(self.pclTitle, -1, wx.ALIGN_CENTER|wx.TOP|wx.LEFT, 20),
			(self.pclPanel, -1, wx.TOP|wx.RIGHT|wx.EXPAND, 20),
			(wx.Panel(self), -1, wx.TOP, 40),
			(self.saveBtn, -1, wx.TOP, 40),
			(wx.Panel(self), -1, wx.TOP, 10),
		]);
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
		self.piiValue.SetValue(self.getDefaultPii());
		self.saveBtn.Enable(False);
		pass;

	def createPipInstallImage(self):
		self.piiTitle = wx.StaticText(self, label = "PIP安装镜像：");
		self.piiTitle.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		# PIP安装镜像值
		self.piiValue = wx.ComboBox(self, value = self.getDefaultPii(), choices = self.getPiiKeyList(), style = wx.CB_READONLY);
		self.piiValue.Bind(wx.EVT_COMBOBOX, self.onPiiCombobox);
		
	def createSaveBtn(self):
		self.saveBtn = wx.Button(self, label = "保存配置", size = (80, 28));
		def onSaveButton(event):
			self.getCtr().saveSettingCfg();
			self.saveBtn.Enable(False);
		self.saveBtn.Bind(wx.EVT_BUTTON, onSaveButton);
		self.saveBtn.Enable(False);
	
	def activeSaveBtn(self):
		self.saveBtn.Enable();
		pass;

	def getDefaultPii(self):
		piiVal = self.getCtr().getSettingCfg("pip_install_image", "");
		for pii in _GG("AppConfig").get("piiList", []):
			if pii["val"] == piiVal:
				return pii["key"];
		return "";

	def getPiiKeyList(self):
		ret = [];
		for pii in _GG("AppConfig").get("piiList", []):
			ret.append(pii["key"]);
		return ret;

	def onPiiCombobox(self, event = None):
		for pii in _GG("AppConfig").get("piiList", []):
			if pii["key"] == self.piiValue.GetValue():
				self.getCtr().setSettingCfg("pip_install_image", pii["val"]);
				break;

	def createPageCountLimit(self):
		self.pclTitle = wx.StaticText(self, label = "标签页数限制：");
		self.pclTitle.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		# 标签页数限制
		defaultVal = self.getCtr().getSettingCfg("fixed_page_count_limit", _GG("AppConfig").get("fixedPageCntLimit", 8));
		self.pclPanel = wx.Panel(self);
		self.pclValue = wx.StaticText(self.pclPanel, label = str(defaultVal));
		btn = wx.Button(self.pclPanel, label = "更改", size = (40, 20));
		def onChangeButton(event):
			maxLimit = 21;
			ned = wx.NumberEntryDialog(self, "更改标签页数限制", "请输入数字", "更改配置", int(defaultVal), 1, maxLimit);
			if ned.ShowModal() == wx.ID_OK:
				val = ned.GetValue();
				self.pclValue.SetLabel(str(val));
				self.getCtr().setSettingCfg("fixed_page_count_limit", val);
		btn.Bind(wx.EVT_BUTTON, onChangeButton);
		# 布局
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.pclValue);
		box.Add(btn, flag = wx.LEFT, border = 10);
		self.pclPanel.SetSizer(box);