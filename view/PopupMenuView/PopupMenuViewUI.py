# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 18:59:05
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-08-11 19:27:46

import wx;

from _Global import _GG;
from function.base import *;

class PopupMenuViewUI(object):
	"""docstring for PopupMenuViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None):
		super(PopupMenuViewUI, self).__init__();
		self.className_ = PopupMenuViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.popupViews = {};

	def getCtr(self):
		return self.viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self.curPath + "***View"); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		pass;

	def createMenuByKey(self, key):
		self.popupViews[key] = wx.Menu();
		pass;

	def getMenuByKey(self, key):
		return self.popupViews[key];

	def appendMenuItem(self, key, menuType = "", title = "", callback = None, itemId = None, params = {}):
		if menuType == "normal":
			if not itemId:
				itemId = wx.NewId();
			menuItem = wx.MenuItem(self.popupViews[key], itemId, title, **params);
			self.popupViews[key].Bind(wx.EVT_MENU, callback, menuItem);
		elif menuType == "separator":
			menuItem = wx.MenuItem(self.popupViews[key], wx.NewId(), kind = wx.ITEM_SEPARATOR);
		self.popupViews[key].Append(menuItem);
		return menuItem;
