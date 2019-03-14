# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 10:49:59
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 17:35:21

import wx;

from _Global import _GG;
from _Global import isExist_G;

from ParentWindowUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.SHOW_SEARCH_PANEL_EVENT : "showSearchPanelWindow",
		G_EVENT.ESC_DOWN_EVENT : "onEscDownEvent",
	};

class ParentWindowCtr(object):
	"""docstring for ParentWindowCtr"""
	def __init__(self, parent = None, params = {}):
		super(ParentWindowCtr, self).__init__();
		self.className_ = ParentWindowCtr.__name__;
		self.curPath = _GG("g_CommonPath") + "window/ParentWindow/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent);
		self.registerEventMap(); # 注册事件
		self.bindEvents(); # 绑定界面事件
		self.escDownEventList = []; # ESC按键事件列表
		self.clientWinSizeEventDict = {}; # 窗口大小事件字典

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		if isExist_G(): # window控制类中的析构函数，涉及到全局变量时，要判断全局变量是否存在
			self.unregisterEventMap(); # 注销事件
			_GG("TimerManager").clearAllTimer(); # 清除所有定时器
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent = None):
		# 创建视图UI类
		windowTitle = _GG("AppConfig")["AppTitle"];
		windowSize = _GG("AppConfig")["AppSize"];
		windowStyle = wx.DEFAULT_FRAME_STYLE|wx.FRAME_NO_WINDOW_MENU; # wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.CLOSE_BOX);
		self.UI = ParentWindowUI(parent, id = -1, title = windowTitle, size = windowSize, style = windowStyle, curPath = self.curPath, windowCtr = self);
		self.UI.initWindow();

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
			
	def updateWindow(self, data):
		self.UI.updateWindow(data);

	def bindEvents(self):
		self.UI.Bind(wx.EVT_SIZE, self.onWinSize);
		self.bindClientWinSizeEvents();
		pass;

	def onWinSize(self, event):
		self.UI.ClientWindow.Size = self.UI.Size;

	# 客户（父）窗口大小变化事件回调
	def onClientWinSize(self, event):
		for objId in self.clientWinSizeEventDict:
			if self.clientWinSizeEventDict[objId]["obj"]:
				for funcId in self.clientWinSizeEventDict[objId]["funcDict"]:
					self.clientWinSizeEventDict[objId]["funcDict"][funcId](event);
		# 重置PreUISize
		self.PreUISize = self.UI.Size;

	# 绑定客户（父）窗口大小变化事件
	def bindClientWinSizeEvents(self):
		self.PreUISize = self.UI.Size;
		self.UI.ClientWindow.Bind(wx.EVT_SIZE, self.onClientWinSize);

	# 绑定事件到客户（父）窗口大小变化事件列表中
	def bindEventToClientWinSize(self, obj, func):
		if callable(func):
			objId = id(obj);
			if objId not in self.clientWinSizeEventDict:
				self.clientWinSizeEventDict[objId] = {"obj" : obj, "funcDict" : {}};
			self.clientWinSizeEventDict[objId]["funcDict"][id(func)] = func;

	# 从客户（父）窗口大小变化事件列表中解绑事件
	def unbindEventToClientWinSize(self, obj, func = None):
		objId = id(obj);
		if objId in self.clientWinSizeEventDict:
			if not func:
				self.clientWinSizeEventDict.pop(objId);
			elif callable(func):
				funcId = id(func);
				if funcId in self.clientWinSizeEventDict[objId]["funcDict"]:
					self.clientWinSizeEventDict[objId]["funcDict"].pop(funcId);

	# 根据ID设置当前窗口（设置成功则返回True）
	def SetActiveChildById(self, wID):
		curActiveChild = self.UI.GetActiveChild();
		# 判断是否有当前节点
		if curActiveChild:
			if curActiveChild.GetId() == wID:
				return False; # 如果当前的窗口ID与wID相同，则直接return
			while True:
				# 循环遍历并更新当前窗口
				self.UI.ActivateNext();
				if self.UI.GetActiveChild().GetId() == wID:
					return True;
				elif self.UI.GetActiveChild().GetId() == curActiveChild.GetId():
					break;
		return False;

	# 显示搜索面板窗口
	def showSearchPanelWindow(self, data):
		curActiveChild = self.UI.GetActiveChild();
		if not hasattr(self, "SearchPanelWindowCtr"):
			if curActiveChild:
				self.appendEventToEscDown(self.SetActiveChildById, curActiveChild.GetId());
			# 创建搜索面板
			self.SearchPanelWindowCtr = CreateCtr(_GG("g_CommonPath") + "window/SearchPanelWindow", self.UI);
			# 根据父窗口大小获取中心位置
			centerPos = self.SearchPanelWindowCtr.getCenterPosByParentSize(self.UI.GetSize());
			self.SearchPanelWindowCtr.getUI().SetPosition((centerPos[0], 0)); # 重置窗口的位置
		else:
			self.SearchPanelWindowCtr.clearWindow(); # 清除窗口内容
			if curActiveChild and curActiveChild.GetId() != self.SearchPanelWindowCtr.getUI().GetId():
				# 根据ID设置当前窗口（设置成功则返回True）
				if self.SetActiveChildById(self.SearchPanelWindowCtr.getUI().GetId()):
					self.appendEventToEscDown(self.SetActiveChildById, curActiveChild.GetId());
		
	# 添加ESC按键事件
	def appendEventToEscDown(self, function, data = None):
		self.escDownEventList.append({"function" : function, "data" : data});
		pass;

	# ESC按键事件回调
	def onEscDownEvent(self, data):
		if len(self.escDownEventList) > 0:
			escDownEvent = self.escDownEventList.pop();
			if "function" in escDownEvent and callable(escDownEvent["function"]):
				if escDownEvent["data"]:
					escDownEvent["function"](escDownEvent["data"]);
				else:
					escDownEvent["function"]();