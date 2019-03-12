# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 14:46:20
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-06 22:48:19

import wx;

from _Global import _GG;

from WindowLeftViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class WindowLeftViewCtr(object):
	"""docstring for WindowLeftViewCtr"""
	def __init__(self, parent, params = {}):
		super(WindowLeftViewCtr, self).__init__();
		self.className_ = WindowLeftViewCtr.__name__;
		self.curPath = _GG("g_CommonPath") + "view\\WindowLeftView\\";
		self.__CtrMap = {}; # 所创建的控制器
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
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
		self.UI = WindowLeftViewUI(parent, curPath = self.curPath, viewCtr = self);
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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "configParseBehavior/XmlConfigParseBehavior", "basePath" : _GG("g_CommonPath") + "behavior\\"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.UI.updateView(data);

	def setTreeItemDictByItem(self, treeItem, itemDict):
		for treeElem in treeItem.getchildren():
			if treeElem.tag == "treeItem":
				treeItemDict = {};
				for k,v in treeElem.attrib.items():
					treeItemDict[k] = v;
				self.setTreeItemDictByItem(treeElem, treeItemDict);
				if "items" not in itemDict:
					itemDict["items"] = [];
				itemDict["items"].append(treeItemDict);
			elif treeElem.tag == "pageData":
				itemDict["pageData"] = {};
				for pageInfo in treeElem.getchildren():
					for k,v in pageInfo.attrib.items():
						itemDict["pageData"][k] = v;
					if pageInfo.tag == "id":
						itemDict["pageData"][pageInfo.tag] = int(pageInfo.text);
					else:
						itemDict["pageData"][pageInfo.tag] = pageInfo.text;

	def getTreeItemsDataByFilePath(self, filePath = None):
		treeItemsData = [];
		if filePath and hasattr(self, "getElementTreesByFilePath"):
			trees = self.getElementTreesByFilePath(filePath);
			for treeElem in trees.getroot():
				if treeElem.tag == "treeItem":
					treeItemDict = {};
					for k,v in treeElem.attrib.items():
						treeItemDict[k] = v;
					self.setTreeItemDictByItem(treeElem, treeItemDict);
					treeItemsData.append(treeItemDict);
		return treeItemsData;
		