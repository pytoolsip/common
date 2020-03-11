# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2020-01-11 17:27:27
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-07 00:14:24
import os;
import wx;
from copy import deepcopy;

from _Global import _GG;

from SettingDialogUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateDialog",
	};

class SettingDialogCtr(object):
	"""docstring for SettingDialogCtr"""
	def __init__(self, parent, params = {}):
		super(SettingDialogCtr, self).__init__();
		self._className_ = SettingDialogCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.init(); # 初始化变量
		self.initUI(parent, params); # 初始化视图UI
	
	def init(self):
		self.__settingCfg = {}; # 设置配置

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
		self.__ui = SettingDialogUI(parent, curPath = self._curPath, viewCtr = self, params = params);
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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "ConfigParseBehavior/JsonConfigBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateDialog(self, data):
		self.__ui.updateDialog(data);
		
	def resetDialog(self):
		self.__settingCfg = {};
		self.__ui.resetDialog();

	def getSettingCfg(self, key, default = None):
		if not self.__settingCfg and os.path.exists(_GG("g_DataPath")+"config/setting_cfg.json"):
			cfg = self.readJsonFile(_GG("g_DataPath")+"config/setting_cfg.json");
			if cfg:
				self.__settingCfg = cfg;
		return self.__settingCfg.get(key, default);

	def setSettingCfg(self, key, val):
		self.__settingCfg[key] = val;
		self.getUI().activeSaveBtn();
	
	# 保存设置
	def saveSettingCfg(self):
		self.writeJsonFile(_GG("g_DataPath")+"config/setting_cfg.json", self.__settingCfg);
		_GG("EventDispatcher").dispatch(_GG("EVENT_ID").SAVE_IP_CONFIG, deepcopy(self.__settingCfg));
