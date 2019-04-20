# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-04-20 12:29:23
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 13:21:07

import wx;
from wx import html;
from wx import html2;

from _Global import _GG;
from function.base import *;

class SearchToolViewUI(wx.Panel):
	"""docstring for SearchToolViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(SearchToolViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = SearchToolViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unbindEvents();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : _GG("WindowObject").GetToolWinSize(),
			"style" : wx.BORDER_NONE,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def bindEvents(self):
		_GG("WindowObject").BindEventToToolWinSize(self, self.onToolWinSize);

	def unbindEvents(self):
		_GG("WindowObject").UnbindEventToToolWinSize(self);

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createWebView();
		pass;
		
	def initViewLayout(self):
		boxSizer = wx.BoxSizer(wx.VERTICAL);
		boxSizer.Add(self.__webView);
		self.SetSizerAndFit(boxSizer)
		pass;

	def updateView(self, data):
		pass;

	def createWebView(self):
		# self.__webView = html2.WebView.New(self, url = _GG("AppConfig")["SearchToolUrl"], size = self.GetSize());
		self.__webView = html.HtmlWindow(self, size = self.GetSize());
		self.__webView.LoadPage(_GG("AppConfig")["SearchToolUrl"]);

	def onToolWinSize(self, sizeInfo, event = None):
		self.SetSize(self.GetSize() + sizeInfo["preDiff"]);
		self.__webView.SetSize(self.__webView.GetSize() + sizeInfo["preDiff"]);
		self.__webView.Layout();
		self.Layout();
		pass;