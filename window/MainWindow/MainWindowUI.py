# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-07-29 10:53:54
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 19:01:48

import wx;

from _Global import _GG;
from function.base import *;

class MainWindowUI(wx.MDIChildFrame):
	"""docstring for MainWindowUI"""
	def __init__(self, parent, id = -1, title = "", pos = (0,0), size = (0,0), style = wx.DEFAULT_FRAME_STYLE, curPath = "", windowCtr = None):
		super(MainWindowUI, self).__init__(parent, id, title = title, pos = pos, size = size, style = style);
		self.className_ = MainWindowUI.__name__;
		self._curPath = curPath;
		self.__windowCtr = windowCtr;

	def getCtr(self):
		return self.__windowCtr;

	def initWindow(self):
		self.createViewCtrs();
		self.initWindowLayout();
		self.Show(True);

	def createSplitterWindows(self):
		self.splitter = wx.SplitterWindow(self, -1, size = (_GG("AppConfig")["AppSize"][0]/3, _GG("AppConfig")["AppSize"][1]));
		self.splitter.SetMinimumPaneSize(10);
		pass;

	def toSplitterWindows(self):
		self.splitter.SplitVertically(self.getCtr().getUIByKey("WindowLeftViewCtr"),
			self.getCtr().getUIByKey("WindowRightViewCtr"));
		pass;

	def createWindowLeftView(self):
		self.getCtr().createCtrByKey("WindowLeftViewCtr", self._curPath + "WindowLeftView", parent = self.splitter);
		pass;

	def createRightWindow(self):
		self.getCtr().createCtrByKey("WindowRightViewCtr", self._curPath + "WindowRightView", parent = self.splitter);
		pass;

	def createViewCtrs(self):
		self.createSplitterWindows();
		self.createWindowLeftView();
		self.createRightWindow();
		self.toSplitterWindows();
		pass;

	def initWindowLayout(self):
		pass;

	def updateWindow(self, data):
		pass;
