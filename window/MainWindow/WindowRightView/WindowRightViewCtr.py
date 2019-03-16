# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 18:09:36
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:18

import wx;

from _Global import _GG;

from WindowRightViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.UPDATE_WINDOW_RIGHT_VIEW : "updateView",
	};

class WindowRightViewCtr(object):
	"""docstring for WindowRightViewCtr"""
	def __init__(self, parent, params = {}):
		super(WindowRightViewCtr, self).__init__();
		self._className_ = WindowRightViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent); # 初始化视图UI
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

	def initUI(self, parent):
		# 创建视图UI类
		self.__ui = WindowRightViewUI(parent, curPath = self._curPath, viewCtr = self);
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
		# self.__ui.updateView(data);
		if "creatPage" in data and data["creatPage"] == True:
			self.createPageToNoteBook(data);
		pass;

	def createPageToNoteBook(self, data):
		if("id" in data) and ("pagePath" in data) and ("title" in data):
			self.getCtrByKey("NoteBookViewCtr").createPageToNoteBook(data["id"], data["pagePath"], data["title"]);
		pass;
