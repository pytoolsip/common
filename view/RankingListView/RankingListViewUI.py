# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-08 22:49:10
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 18:00:25

import wx;

from _Global import _GG;
from function.base import *;
from ui import TitleDetailText;

class RankingListViewUI(wx.ScrolledWindow):
	"""docstring for RankingListViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(RankingListViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = RankingListViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.listDataList = [];
		self.currentItem = None;
		self.SetScrollbars(1, 1, *self.__params["size"]); # 初始化滚动条参数
		self.createTimers(); # 创建定时器

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.stopAllTimer(isDestroy = True); # 停止所有定时器

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"title" : "排行榜",
			"itemBlurColor" : wx.Colour(250,250,250),
			"itemFocusColor" : wx.Colour(210,210,210),
			"fgColourList" : [
				wx.Colour(250,0,0),
				wx.Colour(250,127,80),
				wx.Colour(250,185,15),
			],
			"defaultFgColour" : wx.Colour(100,100,100),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.SetBackgroundColour(self.__params["itemBlurColor"]); # 设置背景颜色

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self.curPath + "***View"); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		self.SetSizer(wx.BoxSizer(wx.VERTICAL))

	def updateView(self, data):
		if "listData" in data:
			self.updateListView(data["listData"]);
		pass;

	def createTimers(self):
		# 创建显示提示定时回调
		self.updateItemBgColorTimer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onUpdateItemBgColorTimer, self.updateItemBgColorTimer);

	def stopAllTimer(self, isDestroy = False):
		if hasattr(self, "updateItemBgColorTimer") and self.updateItemBgColorTimer.IsRunning():
			self.updateItemBgColorTimer.Stop();
			if isDestroy:
				del self.updateItemBgColorTimer;

	def updateListView(self, listData):
		self.clearItems();
		self.createItems(listData);

	def clearItems(self):
		self.GetSizer().Clear(True);
		self.listDataList = [];

	def createItems(self, listData):
		height = 0;
		# 添加item
		for itemData in listData:
			item = self.createItem(itemData);
			self.GetSizer().Add(item, flag = wx.TOP, border = 2);
			self.updateItemForegroundColor(item);
			self.listDataList.append(itemData);
			height += item.GetSize()[1];
		# 更新面板布局
		self.GetSizer().Layout();
		self.SetSize(self.GetSize().x, height);
		self.Layout();

	def createItem(self, itemData):
		item = wx.Panel(self, size = (self.GetSize().x, -1), style = wx.BORDER_THEME);
		self.createIndex(item, itemData["index"]);
		self.createNum(item, itemData["num"]);
		self.createTitleDetail(item, itemData);
		self.initItemLayout(item);
		return item;

	def createIndex(self, item, index):
		item.index = wx.StaticText(item, label = str(index));

	def createNum(self, item, num):
		# 转换数字格式
		if hasattr(self.getCtr(), "formtNumToChStr"):
			num = self.getCtr().formtNumToChStr(num);
		item.num = wx.StaticText(item, label = str(num));

	def createTitleDetail(self, item, itemData):
		width = self.GetSize()[0] - item.index.GetSize()[0] - item.num.GetSize()[0] - 20;
		params = {"size" : (width, -1)};
		for k,v in itemData.items():
			params[k] = v;
		item.titleDetail = TitleDetailText(item, params = params);
		self.bindEventToItem(item.titleDetail);

	def initItemLayout(self, item):
		boxSizer = wx.BoxSizer(wx.HORIZONTAL);
		boxSizer.Add(item.index, flag = wx.TOP|wx.RIGHT, border = 2);
		boxSizer.Add(item.titleDetail, flag = wx.LEFT|wx.RIGHT, border = 2);
		boxSizer.Add(item.num, flag = wx.TOP|wx.LEFT, border = 2);
		item.SetSizer(boxSizer);

	def bindEventToItem(self, item):
		item.onClick = self.onClickItem; # 设置Item的点击回调函数
		item.onEnter = self.onEnterItem; # 设置Item的鼠标进入回调函数

	def onClickItem(self, item, event):
		_GG("Log").d("----onClickItem----");
		pass;

	def onEnterItem(self, item, event):
		if self.currentItem != item:
			if self.currentItem:
				self.currentItem.updateBackgroundColor(self.__params["itemBlurColor"]);
			self.currentItem = item; # 重置当前Item
			self.currentItem.updateBackgroundColor(self.__params["itemFocusColor"]);
			self.updateItemBgColorTimer.Start(200); # 启动更新背景颜色定时器

	def onUpdateItemBgColorTimer(self, event):
		if not self.currentItem.isPointInItemRect(wx.GetMousePosition()): # 判断鼠标位置是否在节点内
			self.currentItem.updateBackgroundColor(self.__params["itemBlurColor"]);
			self.currentItem = None;
			self.updateItemBgColorTimer.Stop();

	def updateItemForegroundColor(self, item):
		childrenNum = len(self.GetSizer().GetChildren());
		if childrenNum > 0 and childrenNum <= len(self.__params["fgColourList"]):
			wxColor = self.__params["fgColourList"][childrenNum - 1];
		else:
			wxColor = self.__params["defaultFgColour"];
		item.index.SetForegroundColour(wxColor);
		item.num.SetForegroundColour(wxColor);
		item.titleDetail.updateForegroundColor(wxColor);
