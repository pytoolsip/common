# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 17:27:44
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-29 18:31:31

from _Global import _GG;

from TreeItemsViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.UPDATE_TREE_ITEMS : "updateView",
	};

class TreeItemsViewCtr(object):
	"""docstring for TreeItemsViewCtr"""
	def __init__(self, parent, params = {}):
		super(TreeItemsViewCtr, self).__init__();
		self._className_ = TreeItemsViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.initParams(params); # 初始化相关参数/属性
		self.getUI().createTreeItems(params.get("itemsData", []));

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
		self.__ui = TreeItemsViewUI(parent, curPath = self._curPath, viewCtr = self);
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
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		# 判断要更新视图的类型ID
		if self.__type and ("type" in data):
			if data["type"] != self.__type:
				return; # 若不需要更新当前视图，则直接返回，不执行更新逻辑
		self.getUI().updateView(data);

	def initParams(self, params):
		# 树节点的页面数据字典
		self.__itemPageDataDict = {};
		# 用于标记当前类的类型ID
		self.__type = params.get("type", None);
		# 选中树节点的回调
		self.__onActivated = params.get("onActivated", None);
		pass;

	def bindEventToItem(self, treeCtr, item, itemInfo, pathList):
		if "key" in itemInfo:
			basePath = _GG("g_ProjectPath") + itemInfo["trunk"] + "/";
			if "branch" in itemInfo:
				basePath += itemInfo["branch"] + "/";
			self.__itemPageDataDict[item] = {
				"key" : itemInfo["key"],
				"pagePath" : (basePath + itemInfo["path"]).replace("/", "/"),
				"category" : "/".join(pathList),
				"title" : itemInfo.get("title", itemInfo["name"]),
			};
		pass;

	def onActivated(self, event):
		item = event.GetItem();
		if item in self.__itemPageDataDict and callable(self.__onActivated):
			self.__onActivated(self.__itemPageDataDict[item]);

	def getItemPageData(self, itemKey):
		for pageData in self.__itemPageDataDict.values():
			if pageData["key"] == itemKey:
				return pageData;
		return {};

