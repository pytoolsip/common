# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 18:09:36
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:19

import wx;

from _Global import _GG;
from function.base import *;

class WindowRightViewUI(wx.Panel):
	"""docstring for WindowRightViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None):
		super(WindowRightViewUI, self).__init__(parent, id);
		self._className_ = WindowRightViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.createNoteBookCtr();
		pass;
		
	def initViewLayout(self):
		hBox = wx.BoxSizer(wx.HORIZONTAL);
		hBox.Add(self.getCtr().getUIByKey("NoteBookViewCtr"), 1, wx.EXPAND);
		self.SetSizerAndFit(hBox);
		pass;

	def updateView(self, data):
		pass;

	def createNoteBookCtr(self):
		self.getCtr().createCtrByKey("NoteBookViewCtr", _GG("g_CommonPath") + "view/NoteBookView"); # , parent = self, params = {}
		pass;