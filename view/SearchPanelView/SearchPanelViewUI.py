# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-26 14:05:42
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-03 22:24:41

import wx;

from _Global import _GG;
from function.base import *;
from ui import TitleDetailText, ScrollWindow;

class SearchPanelViewUI(ScrollWindow):
	"""docstring for SearchPanelViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, size = (0,0)):
		super(SearchPanelViewUI, self).__init__(parent, id = id, params = {"size" : size});
		self._className_ = SearchPanelViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.currentItem = None;

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.stopAllTimer(isDestroy = True); # 停止所有定时器

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.initContentSizer(); # 初始化内容sizer
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.createTimers(); # 创建定时器

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		self.updateSearchResult(data);
		pass;

	def createTimers(self):
		# 创建显示提示定时回调
		self.updateItemBgColorTimer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onUpdateItemBgColorTimer, self.updateItemBgColorTimer);

	def stopAllTimer(self, isDestroy = False):
		if self.updateItemBgColorTimer.IsRunning():
			self.updateItemBgColorTimer.Stop();
			if isDestroy:
				del self.updateItemBgColorTimer;

	def initContentSizer(self):
		self.contentView.SetSizer(wx.BoxSizer(wx.VERTICAL));
		pass;

	def clearView(self):
		if hasattr(self, "contentView") and self.contentView:
			self.contentView.GetSizer().Clear(True);

	def updateSearchResult(self, data):
		# 清空视图
		self.clearView();
		# 创建搜索结果项
		self.createSearchResultItemList(data);

	def createSearchResultItemList(self, data):
		# 添加搜索结果项到Sizer
		dataCount = 0;
		searchResultPanelHeight = 0
		for itemData in data:
			dataCount += 1;
			# 创建text
			text = TitleDetailText(self.contentView, -1, {
				"size" : (self.contentView.GetSize()[0], 20),
				"title" : itemData["name"],
				"detail" : itemData["path"],
			});
			text.itemData = itemData; # 保存节点数据
			text.SetBackgroundColour(_GG("AppConfig")["searchItemBlurColor"]);
			self.bindEventToSearchItem(text);
			self.contentView.GetSizer().Add(text);
			searchResultPanelHeight += text.GetSize()[1];
			if dataCount < len(data):
				# 创建line
				line = wx.StaticLine(self.contentView, size = (self.contentView.GetSize()[0],-1));
				self.contentView.GetSizer().Add(line);
				searchResultPanelHeight += line.GetSize()[1];
		# 更新搜索结果面板布局
		self.contentView.GetSizer().Layout();
		# 更新搜索结果面板大小
		self.contentView.SetSize(self.contentView.GetSize()[0], searchResultPanelHeight);
		self.contentView.Layout();

	def bindEventToSearchItem(self, item):
		# 设置Item的回调函数
		item.onClick = self.onClickItem;
		item.onEnter = self.onEnterItem;

	def onEnterItem(self, item, event):
		if self.currentItem != item:
			if self.currentItem:
				self.currentItem.updateBackgroundColor(_GG("AppConfig")["searchItemBlurColor"]);
			self.currentItem = item; # 重置当前Item
			self.currentItem.updateBackgroundColor(_GG("AppConfig")["searchItemFocusColor"]);
			self.updateItemBgColorTimer.Start(200); # 启动更新背景颜色定时器

	def onUpdateItemBgColorTimer(self, event):
		if not self.currentItem.isPointInRect(wx.GetMousePosition()): # 判断鼠标位置是否在节点内
			self.currentItem.updateBackgroundColor(_GG("AppConfig")["searchItemBlurColor"]);
			self.currentItem = None;
			self.updateItemBgColorTimer.Stop();

	def onClickItem(self, item, event):
		data = {
			"createPage" : True,
			"key" : item.itemData["key"],
			"pagePath" : item.itemData["pagePath"],
			"category" : item.itemData["category"],
			"title" : item.itemData["name"],
		};
		_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_WINDOW_RIGHT_VIEW, data);
		_GG("EventDispatcher").dispatch(_GG("EVENT_ID").ESC_DOWN_EVENT, {}); # 隐藏搜索面板【相当于按ESC键】
