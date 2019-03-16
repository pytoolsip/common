# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-03 17:07:37
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:09

import wx;
import math;

from _Global import _GG;
from function.base import *;
from ui import TitleSketchText;

class SketchGridViewUI(wx.Panel):
	"""docstring for SketchGridViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params)
		super(SketchGridViewUI, self).__init__(parent, id);
		self._className_ = SketchGridViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.gridDataList = [];
		self.currentItem = None;
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
			# "cols" : 2,
			"minCols" : 1,
			"itemSize" : (200,200),
			"itemBlurColor" : wx.Colour(250,250,250),
			"itemFocusColor" : wx.Colour(210,210,210),
		};
		for k,v in params.items():
			self.__params[k] = v;
		# 校验cols
		self.checkCols();
		# 校验尺寸
		itemSize = self.__params["itemSize"];
		self.__params["itemSize"] = (max(1, itemSize[0]), max(1, itemSize[1]))

	def checkCols(self):
		if self.__params["minCols"] <= 0:
			self.__params["minCols"] = 1;
		if "cols" not in self.__params or self.__params["cols"] < self.__params["minCols"]:
			self.__params["cols"] = self.__params["minCols"];
			return False;
		return True;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.SetBackgroundColour(self.__params["itemBlurColor"]); # 设置背景颜色

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		gridSizer = wx.GridSizer(self.__params["cols"]);
		self.SetSizer(gridSizer);
		pass;

	def updateView(self, data):
		if "gridData" in data:
			if "isAdd" in data and data["isAdd"] == True:
				self.addGridView(data["gridData"]);
			else:
				self.updateGridView(data["gridData"]);
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

	def updateGridView(self, gridData, border = 0):
		self.clearItems();
		self.createItems(gridData, border = border);

	def clearItems(self):
		self.GetSizer().Clear(True);
		self.gridDataList = [];

	def createItems(self, gridData, oriRows = 0, border = 0):
		# 重置rows
		self.GetSizer().SetRows(oriRows + math.ceil(len(gridData)/self.GetSizer().GetCols()));
		# 添加item
		for itemData in gridData:
			params = {"size" : self.__params["itemSize"]};
			for k,v in itemData.items():
				params[k] = v;
			item = TitleSketchText(self, params = params);
			self.bindEventToItem(item);
			self.GetSizer().Add(item, flag = wx.LEFT|wx.RIGHT, border = border);
			self.gridDataList.append(itemData);
		# 更新面板布局
		self.GetSizer().Layout();
		# 更新面板大小
		self.SetSize(self.GetSizer().GetCols() * self.__params["itemSize"][0],
		 self.GetSizer().GetRows() * self.__params["itemSize"][1])
		self.Layout();

	def bindEventToItem(self, item):
		item.onClick = self.onClickItem; # 设置Item的点击回调函数
		item.onEnter = self.onEnterItem; # 设置Item的鼠标进入回调函数

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

	def onClickItem(self, item, event):
		_GG("Log").d("SketchGridView -> onClickItem")

	def addGridView(self, gridData):
		self.createItems(gridData, self.GetSizer().GetRows());

	def updateViewSize(self, size):
		cols = math.floor(size.x/self.__params["itemSize"][0]);
		self.__params["cols"] = cols;
		# 获取边界值
		border = 0;
		# 校验cols
		if self.checkCols():
			border = max(0, (size.x - self.__params["cols"]) / self.__params["cols"] - self.__params["itemSize"][0]);
		self.GetSizer().SetCols(self.__params["cols"]);
		self.updateGridView(self.gridDataList, border = border/2);