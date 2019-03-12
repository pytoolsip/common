# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-10-27 15:47:32
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-01-27 18:22:31

import wx;

class InfoInputView(wx.Panel):
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(InfoInputView, self).__init__(parent, id, size = self.__params["size"]);
		self.createControls();
		self.initViewLayout();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : (200,200),
			"name" : "名称",
			"tips" : "*（必填）",
			"exTips" : "提示信息",
			"inputSize" : (-1,20),
			"inputStyle" : wx.TE_PROCESS_TAB,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def createControls(self):
		self.createName();
		self.createInput();
		self.createTips();
		self.createExTips();

	def initViewLayout(self):
		box = wx.FlexGridSizer(3,2,0);
		# 添加第一行
		box.AddMany([
			(self.__name, 2, wx.LEFT|wx.RIGHT, 6),
			(self.__input, 1, wx.EXPAND),
			(self.__tips, 2, wx.LEFT, 6),
		]);
		# 添加第二行
		box.AddMany([
			(wx.Panel(self)), # 用于占位
			(self.__exTips, 2, wx.TOP, -2),
		]);
		box.AddGrowableCol(1, proportion = 1);
		box.AddGrowableRow(1, proportion = 1);
		self.SetSizerAndFit(box);

	def createName(self):
		self.__name = wx.StaticText(self, label = self.__params["name"]);

	def createInput(self):
		self.__input = wx.TextCtrl(self, -1, "", size = self.__params["inputSize"], style = self.__params["inputStyle"]);
		self.__input.Bind(wx.EVT_TEXT, self.__onInput__);

	def createTips(self):
		self.__tips = wx.StaticText(self, label = self.__params["tips"]);

	def createExTips(self):
		self.__exTips = wx.StaticText(self, label = self.__params["exTips"]);
		self.__exTips.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL));
		wx.CallAfter(self.__exTips.Hide);

	def __onInput__(self, event):
		if hasattr(self, "onInput"):
			self.onInput(self, self.getInputValue());

	def getInputValue(self):
		return self.__input.GetValue();

	def showExTips(self, wxColor = None):
		if not self.__exTips.IsShown():
			self.__exTips.Show();
		if wxColor:
			self.__exTips.SetForegroundColour(wxColor);