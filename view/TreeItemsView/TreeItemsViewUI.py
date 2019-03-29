# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 17:27:44
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-29 21:02:27

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
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		pass;

	def createTreeItemsByItemsData(self, parentItem, itemsData, pathList = []):
		for itemInfo in itemsData:
			pathList.append(itemInfo["name"]);
			item = self.AppendItem(parentItem, itemInfo["name"]);
			if "items" in itemInfo:
				self.createTreeItemsByItemsData(item, itemInfo["items"], pathList = pathList);
			self.getCtr().bindEventToItem(item, itemInfo, pathList);
			pathList.pop();
		pass;

	def createTreeItems(self, itemsData):
		self.createTreeItemsByItemsData(self.AddRoot("root"), itemsData);
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.getCtr().onActivated);

	def checkTreeItem(self, nameList, parentItem = None):
		if not parentItem:
			parentItem = self.GetRootItem();
		if len(nameList) == 0:
			return parentItem;
		item = self.GetFirstChild(parentItem);
		while item.IsOk():
			if self.GetItemText(item) == nameList[0]:
				return self.checkTreeItem(nameList[1:]);
			else:
				item = self.GetNextSibling(item);
		return self.checkTreeItem(nameList[1:], self.AppendItem(parentItem, nameList[0]));

	def removeTreeItem(self, item):
		while item.IsOk():
			parentItem = self.GetItemParent(item);
			self.Delete(item);
			if self.GetChildrenCount(parentItem, recursively = False) == 0:
				item = parentItem;
			else:
				break;
