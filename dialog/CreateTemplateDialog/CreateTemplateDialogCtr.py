# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2020-01-12 13:31:23
# @Last Modified by:   Administrator
# @Last Modified time: 2020-01-12 13:31:23
import os;
import wx;

from _Global import _GG;

from CreateTemplateDialogUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateDialog",
	};

class CreateTemplateDialogCtr(object):
	"""docstring for CreateTemplateDialogCtr"""
	def __init__(self, parent, params = {}):
		super(CreateTemplateDialogCtr, self).__init__();
		self._className_ = CreateTemplateDialogCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.init();

	def init(self):
		self.__modCreator = require(os.path.join(_GG("g_ProjectPath"), "template", "module"), "ModuleCreator", "CreateModuleObj")();
		pass;

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
		self.__ui = CreateTemplateDialogUI(parent, curPath = self._curPath, viewCtr = self, params = params);
		self.__ui.initDialog();

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
			
	def updateDialog(self, data):
		self.__ui.updateDialog(data);
		
	def resetDialog(self):
		self.__ui.resetDialog();

	def getModuleList(self):
		return [
			"behavior",
			"view",
			"window",
			"dialog",
		];
	
	def createMod(self, modName, targetModName, targetModPath):
		_GG("Log").d("CreateTemplateDialogCtr.createMod:", modName, targetModName, targetModPath);
		return self.__modCreator.createMod(modName, targetModName, targetModPath);