# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-10 15:59:49
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-12 17:10:59

import wx;

from _Global import _GG;

from PageGridsViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class PageGridsViewCtr(object):
	"""docstring for PageGridsViewCtr"""
	def __init__(self, parent, params = {}):
		super(PageGridsViewCtr, self).__init__();
		self.className_ = PageGridsViewCtr.__name__;
		self.curPath = _GG("g_CommonPath") + "view\\PageGridsView\\";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件

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

	def initUI(self, parent, params):
		# 创建视图UI类
		self.UI = PageGridsViewUI(parent, curPath = self.curPath, viewCtr = self, params = params);
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


	def updateViewByDefaultData(self):
		self.updateView({"gridsData" : self.getGridData()})

	def getGridData(self):
		return [
			{"title":"工具1", "name":"开发者1", "detail":"详细描述1"},
			{"title":"工具2", "name":"开发者2", "detail":"详细描述2"},
			{"title":"工具3", "name":"开发者3", "detail":"详细描述3"},
			{"title":"工具4", "name":"开发者4", "detail":"详细描述4"},
			{"title":"工具1", "name":"开发者1", "detail":"详细描述1"},
			{"title":"工具2", "name":"开发者2", "detail":"详细描述2"},
			{"title":"工具3", "name":"开发者3", "detail":"详细描述3"},
			{"title":"工具4", "name":"开发者4", "detail":"详细描述4"},
		];