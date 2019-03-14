# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-12 20:18:23
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 17:32:15

import wx;

from _Global import _GG;

from DownPagesViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class DownPagesViewCtr(object):
	"""docstring for DownPagesViewCtr"""
	def __init__(self, parent, params = {}):
		super(DownPagesViewCtr, self).__init__();
		self.className_ = DownPagesViewCtr.__name__;
		self.curPath = _GG("g_CommonPath") + "view/DownPagesView/";
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
		self.UI = DownPagesViewUI(parent, curPath = self.curPath, viewCtr = self, params = params);
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

	def addDownPage(self, page, key, title, params = {}):
		# 添加页面视图
		if isinstance(page, str):
			return self.UI.createDownPageView(page, key, title, params = params);
		elif isinstance(page, wx.Window):
			return self.UI.addDownPageView(page, key, title);
