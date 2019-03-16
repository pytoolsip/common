# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 17:27:44
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:12

import wx;

from _Global import _GG;
from function.base import *;

class TreeItemsViewUI(wx.TreeCtrl):
	"""docstring for TreeItemsViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None):
		super(TreeItemsViewUI, self).__init__(parent, id, style = wx.TR_HIDE_ROOT|wx.TR_LINES_AT_ROOT|wx.TR_HAS_BUTTONS);
		self._className_ = TreeItemsViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.createTreeItems();
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		if "itemsData" in data:
			self.updateTreeItems(data);
		pass;

	def createTreeItems(self):
		self.treeCtrlRoot = self.AddRoot("root");
		pass;

	def createTreeItemsByItemsData(self, parentItem, itemsData, pathList = []):
		for itemInfo in itemsData:
			pathList.append(itemInfo["name"]);
			item = self.AppendItem(parentItem, itemInfo["name"]);
			if "items" in itemInfo:
				self.createTreeItemsByItemsData(item, itemInfo["items"], pathList = pathList);
			if "pageData" in itemInfo:
				self.__viewCtr.bindEventToItem(self, item, itemInfo, pathList);
			pathList.pop();
		pass;

	def updateTreeItems(self, data):
		itemsData = data["itemsData"];
		self.createTreeItemsByItemsData(self.treeCtrlRoot, itemsData);
		pass;
