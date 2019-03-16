# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-10-27 15:47:32
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 11:53:06

import wx;

class DirInputView(wx.Panel):
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(DirInputView, self).__init__(parent, id, size = self.params["size"]);
		self.createControls();
		self.initViewLayout();

	def initParams(self, params):
		# 初始化参数
		self.params = {
			"size" : (-1,-1),
			"inputSize" : (-1,20),
			"buttonSize" : (30,20),
		};
		for k,v in params.items():
			self.params[k] = v;

	def createControls(self):
		self.createInput();
		self.createButton();
		pass;

	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.input, proportion = 1);
		box.Add(self.button, proportion = 0);
		self.SetSizerAndFit(box);

	def createInput(self):
		self.input = wx.TextCtrl(self, -1, "", size = self.params["inputSize"]);

	def createButton(self):
		self.button = wx.Button(self, -1, "选择", size = self.params["buttonSize"]);
		self.button.Bind(wx.EVT_BUTTON, self.onClickButton)

	def onClickButton(self, event):
		dirVal = wx.DirSelector();
		if dirVal != "":
			self.input.SetValue(dirVal);

	def getInputValue(self):
		return self.input.GetValue();

	def resetInputValue(self):
		return self.input.SetValue("");