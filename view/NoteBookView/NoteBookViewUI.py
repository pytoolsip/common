# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 18:27:07
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-11-09 23:16:57

import wx;

from _Global import _GG;
from function.base import *;

class NoteBookViewUI(wx.Notebook):
	"""docstring for NoteBookViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None):
		super(NoteBookViewUI, self).__init__(parent, id);
		self.className_ = NoteBookViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;

	def getCtr(self):
		return self.viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.getCtr().createCtrByKey("PopupMenuViewCtr", _GG("g_CommonPath") + "view\\PopupMenuView"); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		pass;

	def addPage(self, page, title):
		self.AddPage(page, title);
		return self.FindPage(page);