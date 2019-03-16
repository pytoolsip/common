# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-12 20:18:23
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:58

import wx;

from _Global import _GG;
from function.base import *;

class DownPagesViewUI(wx.Panel):
	"""docstring for DownPagesViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(DownPagesViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = DownPagesViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.pageDict = {};

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"title" : "排行榜",
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createTitle();
		self.createNotebook();
		pass;
		
	def initViewLayout(self):
		boxSizer = wx.BoxSizer(wx.VERTICAL);
		boxSizer.Add(self.title, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 2);
		boxSizer.Add(self.noteBook, flag = wx.EXPAND);
		self.SetSizer(boxSizer)

	def updateView(self, data):
		pass;

	def createTitle(self):
		self.title = wx.StaticText(self, label = self.__params["title"]);
		font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD);
		self.title.SetFont(font);

	def createNotebook(self):
		self.noteBook = wx.Notebook(self, size = (self.GetSize().x, self.GetSize().y - self.title.GetSize().y), style = wx.NB_BOTTOM);

	def createDownPageView(self, pagePath, key, title, params = {}):
		self.getCtr().createCtrByKey(key, pagePath, parent = self.noteBook, params = params); # , parent = self, params = {}
		self.noteBook.AddPage(self.getCtr().getUIByKey(key), title);
		self.pageDict[key] = self.getCtr().getUIByKey(key);
		return self.noteBook.FindPage(self.getCtr().getUIByKey(key));

	def addDownPageView(self, pageView, key, title):
		if pageView.Parent != self.noteBook:
			pageView.Reparent(self.noteBook);
		self.noteBook.AddPage(pageView, title);
		self.pageDict[key] = pageView;
		return self.noteBook.FindPage(pageView);
