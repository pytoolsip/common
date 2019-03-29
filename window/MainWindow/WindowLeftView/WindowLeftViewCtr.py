# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 14:46:20
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-29 18:35:34

import wx;

from _Global import _GG;

from WindowLeftViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.LOGIN_SUCCESS_EVENT : "updateUserNameView",
		G_EVENT.UPDATE_WINDOW_LEFT_VIEW : "updateTreeView",
	};

class WindowLeftViewCtr(object):
	"""docstring for WindowLeftViewCtr"""
	def __init__(self, parent, params = {}):
		super(WindowLeftViewCtr, self).__init__();
		self._className_ = WindowLeftViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.initTreeItemsData(); # 初始化树节点数据
		self.initUI(parent); # 初始化视图UI

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
		self.__ui = WindowLeftViewUI(parent, curPath = self._curPath, viewCtr = self);
		self.__ui.initView();

	def getUI(self):
		return self.__ui;

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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "ConfigParseBehavior/JsonConfigBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/UserServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.__ui.updateView(data);

	def initTreeItemsData(self):
		self.__treeItemsData = [];
		if os.path.exists(_GG("g_DataPath")+"tools_tree.json"):
			self.__treeItemsData = self.readJsonFile(_GG("g_DataPath")+"tools_tree.json");

	def updateUserNameView(self, data):
		def onClick():
			# 显示玩家信息的弹窗
			pass;
		self.getCtrByKey("UserNameTextViewCtr").updateView({"name" : data.name, "onClick" : onClick});

	def onClickLogin(self, event):
		self._loginIP_();

	# 创建树控件
	def createTreeCtrl(self):
		def onActivated(pageInfo):
			_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_WINDOW_RIGHT_VIEW, {
				"createPage" : True,
				"key" : pageInfo["key"],
				"pagePath" : pageInfo["pagePath"],
				"category" : pageInfo["category"],
				"title" : pageInfo["title"]
			});
		self.createCtrByKey("TreeItemsViewCtr", _GG("g_CommonPath") + "view/TreeItemsView", parent = self.getUI(), params = {
			"itemsData" : self.__treeItemsData,
			"type" : "WINDOW_LEFT_TREE",
			"onActivated" : onActivated,
		});

	def getFirstItemData(self):
		if len(self.__treeItemsData) > 0:
			return self.__treeItemsData[0];
		return {};

	def getFirstItemPageData(self):
		itemData = self.getFirstItemData();
		return self.getCtrByKey("TreeItemsViewCtr").getItemPageData(itemData.get("key", ""));

	def checkTreeItemsData(self, nameList, treeItemsData):
		name = nameList.pop(0);
		for itemData in treeItemsData:
			if itemData["name"] == name:
				if len(nameList) == 0:
					return itemData;
				if "items" not in itemData:
					itemData["items"] = [];
				return self.checkTreeItemsData(nameList, itemData["items"]);
			pass;
		newItemData = {"name" : name};
		treeItemsData.append(newItemData);
		if len(nameList) == 0:
			return newItemData;
		else:
			newItemData["items"] = [];
			return self.checkTreeItemsData(nameList, newItemData["items"]);


	def updateTreeView(self, data):
		if "key" not in data or "namePath" not in data:
			return;
		if data.get("action", "add"):
