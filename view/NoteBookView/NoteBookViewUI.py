# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 18:27:07
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 19:00:30

import wx;

from _Global import _GG;
from function.base import *;

class NoteBookViewUI(wx.Notebook):
	"""docstring for NoteBookViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None):
		super(NoteBookViewUI, self).__init__(parent, id);
		self.className_ = NoteBookViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.getCtr().createCtrByKey("PopupMenuViewCtr", _GG("g_CommonPath") + "view/PopupMenuView"); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		pass;

	def addPage(self, page, title):
		self.AddPage(page, title);
		return self.FindPage(page);