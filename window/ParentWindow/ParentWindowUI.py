# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 10:49:59
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-11-24 13:07:55

import wx;

from _Global import _GG;
from function.base import *;

class ParentWindowUI(wx.MDIParentFrame):
	"""docstring for ParentWindowUI"""
	def __init__(self, parent, id = -1, title = "", pos = (0,0), size = (0,0), style = wx.DEFAULT_FRAME_STYLE, curPath = "", windowCtr = None):
		super(ParentWindowUI, self).__init__(parent, id, title = title, pos = pos, size = size, style = style);
		self.className_ = ParentWindowUI.__name__;
		self.curPath = curPath;
		self.windowCtr = windowCtr;

	def getCtr(self):
		return self.windowCtr;

	def initWindow(self):
		self.createViewCtrs();
		self.initWindowLayout();
		pass;

	def createViewCtrs(self):
		self.getCtr().createCtrByKey("MenuBarViewCtr", self.curPath + "MenuBarView"); # , parent = self, params = {}
		pass;

	def initWindowLayout(self):
		pass;

	def updateWindow(self, data):
		pass;
