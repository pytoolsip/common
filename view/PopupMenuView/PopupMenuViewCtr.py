# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 18:59:05
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 17:33:21

import wx;

from _Global import _GG;

from PopupMenuViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class PopupMenuViewCtr(object):
	"""docstring for PopupMenuViewCtr"""
	def __init__(self, parent, params = {}):
		super(PopupMenuViewCtr, self).__init__();
		self.className_ = PopupMenuViewCtr.__name__;
		self.curPath = _GG("g_CommonPath") + "view/PopupMenuView/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件

		self.menuItemKeysDict = {};
		self.menuItemKeysList = {};

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unregisterEventMap(); # 注销事件
		self.unbindBehaviors(); # 解绑组件
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent):
		# 创建视图UI类
		self.UI = PopupMenuViewUI(parent, curPath = self.curPath, viewCtr = self);
		self.UI.initView();

	def getUI(self):
		return self.UI;

	"""
		key : 索引所创建控制类的key值
		path : 所创建控制类的路径
		parent : 所创建控制类的UI的父节点，默认为本UI
		params : 扩展参数
	"""
	def createCtrByKey(self, key, path, parent = None, params = {}):
		if not parent:
			parent = self.getUI();
		self.__CtrMap[key] = CreateCtr(path, parent, params = params);

	def getCtrByKey(self, key):
		return self.__CtrMap.get(key, None);

	def getUIByKey(self, key):
		ctr = self.getCtrByKey(key);
		if ctr:
			return ctr.getUI();
		return None;
		
	def registerEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").register(eventId, self, callbackName);

	def unregisterEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").unregister(eventId, self, callbackName);

	def bindBehaviors(self):
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.UI.updateView(data);

	def appendNormalMenuItem(self, key, title, callback, itemId = None, params = {}):
		self.UI.appendMenuItem(key, "normal", title, callback, itemId = itemId, params = params);
		pass;

	def appendSeparatorMenuItem(self, key):
		self.UI.appendMenuItem(key, "separator");
		pass;

	def createNewMenu(self, key, data):
		self.UI.createMenuByKey(key);
		if "itemsData" in data:
			for itemData in data["itemsData"]:
				if "isSeparator" in itemData and itemData["isSeparator"] == True:
					self.appendSeparatorMenuItem(key);
				else:
					itemId = None;
					params = {};
					if "itemId" in itemData:
						itemId = itemData["itemId"];
					if "params" in itemData:
						params = itemData["params"];
					self.appendNormalMenuItem(key, itemData["title"], itemData["callback"], itemId = itemId, params = params);
		pass;

	def getMenu(self, key):
		return self.UI.getMenuByKey(key);
