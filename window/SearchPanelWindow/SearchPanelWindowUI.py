# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-05 21:14:16
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-11-11 16:24:53

import threading;
import wx;

from _Global import _GG;
from function.base import *;

class SearchPanelWindowUI(wx.MDIChildFrame):
	"""docstring for SearchPanelWindowUI"""
	def __init__(self, parent, id = -1, title = "", pos = (0,0), size = (0,0), style = wx.DEFAULT_FRAME_STYLE, curPath = "", windowCtr = None):
		super(SearchPanelWindowUI, self).__init__(parent, id, title = title, pos = pos, size = size, style = style); #^(wx.RESIZE_BORDER|wx.CAPTION)
		self.className_ = SearchPanelWindowUI.__name__;
		self.curPath = curPath;
		self.windowCtr = windowCtr;

	def getCtr(self):
		return self.windowCtr;

	def initWindow(self):
		self.createViewCtrs();
		self.initWindowLayout();
		self.Centre();
		self.Show(True);

	def createViewCtrs(self):
		self.createSearchCtrl();
		self.createSearchStaticLine();
		self.createSearchPanel();
		pass;

	def initWindowLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.searchTextCtrl, proportion = 0, flag = wx.ALL|wx.EXPAND, border = 1);
		box.Add(self.searchStaticLine, proportion = 0, flag = wx.ALL|wx.EXPAND, border = 1);
		box.Add(self.getCtr().getUIByKey("SearchPanelViewCtr"), proportion = 0, flag = wx.ALL|wx.EXPAND, border = 1);
		self.SetSizerAndFit(box);
		pass;

	def createSearchCtrl(self):
		self.searchTextCtrl = wx.TextCtrl(self, -1, value = "", size = (_GG("AppConfig")["SearchPanelSize"][0],-1));
		self.searchTextCtrl.Bind(wx.EVT_TEXT, self.getCtr().onSearchText);

	def createSearchStaticLine(self):
		self.searchStaticLine = wx.StaticLine(self, size = (_GG("AppConfig")["SearchPanelSize"][0],-1));

	def createSearchPanel(self):
		params = {"size" : _GG("AppConfig")["SearchPanelSize"], "bgColor" : _GG("AppConfig")["SearchPanelBGColor"]};
		self.getCtr().createCtrByKey("SearchPanelViewCtr", _GG("g_CommonPath") + "view\\SearchPanelView", params = params);
		pass;

	def updateWindow(self, data):
		pass;

	def clearWindow(self):
		self.searchTextCtrl.SetValue(""); # 重置搜索文本
		self.getCtr().getCtrByKey("SearchPanelViewCtr").clearView(); # 清空视图

