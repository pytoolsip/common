# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-29 22:19:40
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:56
import os;
import wx;

from _Global import _GG;
from _Global import isExist_G;

from TemplateWindowUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateWindow",
	};

class TemplateWindowCtr(object):
	"""docstring for TemplateWindowCtr"""
	def __init__(self, parent = None, params = {}):
		super(TemplateWindowCtr, self).__init__();
		self._className_ = TemplateWindowCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent);
		self.registerEventMap(); # 注册事件

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		if isExist_G(): # window控制类中的析构函数，涉及到全局变量时，要判断全局变量是否存在
			self.unregisterEventMap(); # 注销事件
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent = None):
		# 创建视图UI类
		windowTitle = "TemplateWindow标题";
		windowSize = (960,640); # _GG("AppConfig")["AppSize"];
		windowStyle = wx.DEFAULT_FRAME_STYLE; # wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.CLOSE_BOX);
		self.__ui = TemplateWindowUI(parent, id = -1, title = windowTitle, size = windowSize, style = windowStyle, curPath = self._curPath, windowCtr = self);
		self.__ui.initWindow();

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
			
	def updateWindow(self, data):
		self.__ui.updateWindow(data);