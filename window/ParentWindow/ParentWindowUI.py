# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 10:49:59
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:22

import wx;

from _Global import _GG;
from function.base import *;

class ParentWindowUI(wx.MDIParentFrame):
	"""docstring for ParentWindowUI"""
	def __init__(self, parent, id = -1, title = "", pos = (0,0), size = (0,0), style = wx.DEFAULT_FRAME_STYLE, curPath = "", windowCtr = None):
		super(ParentWindowUI, self).__init__(parent, id, title = title, pos = pos, size = size, style = style);
		self._className_ = ParentWindowUI.__name__;
		self._curPath = curPath;
		self.__windowCtr = windowCtr;

	def getCtr(self):
		return self.__windowCtr;

	def initWindow(self):
		self.initIcon();
		self.createViewCtrs();
		self.initWindowLayout();
		pass;

	def createViewCtrs(self):
		self.getCtr().createCtrByKey("MenuBarViewCtr", self._curPath + "MenuBarView"); # , parent = self, params = {}
		pass;

	def initWindowLayout(self):
		pass;

	def updateWindow(self, data):
		pass;

	def initIcon(self):
		self.SetIcon(wx.Icon(_GG("g_CommonPath")+"/res/img/dzjh.ico", wx.BITMAP_TYPE_ICO));