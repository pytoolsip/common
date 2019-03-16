# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-29 22:19:40
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:57

import wx;

from _Global import _GG;
from function.base import *;

class TemplateWindowUI(wx.Frame):
	"""docstring for TemplateWindowUI"""
	def __init__(self, parent, id = -1, title = "", pos = (0,0), size = (0,0), style = wx.DEFAULT_FRAME_STYLE, curPath = "", windowCtr = None):
		super(TemplateWindowUI, self).__init__(parent, id, title = title, pos = pos, size = size, style = style);
		self._className_ = TemplateWindowUI.__name__;
		self._curPath = curPath;
		self.__windowCtr = windowCtr;

	def getCtr(self):
		return self.__windowCtr;

	def initWindow(self):
		self.createViewCtrs();
		self.initWindowLayout();
		self.Centre();
		self.Show(True);
		pass;

	def createViewCtrs(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		pass;

	def initWindowLayout(self):
		pass;

	def updateWindow(self, data):
		pass;