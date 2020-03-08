# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-07-29 10:53:54
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-06 22:21:06

import wx;

from _Global import _GG;
from _Global import isExist_G;

from MainWindowUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateWindow",
	};

class MainWindowCtr(object):
	"""docstring for MainWindowCtr"""
	def __init__(self, parent = None, params = {}):
		super(MainWindowCtr, self).__init__();
		self._className_ = MainWindowCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.toolWinSizeEventDict = {}; # 窗口大小事件字典
		self.initUI(parent, params);
		self.registerEventMap(); # 注册事件
		self.bindEvents(); # 绑定事件

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		if isExist_G(): # window控制类中的析构函数，涉及到全局变量时，要判断全局变量是否存在
			self.unregisterEventMap(); # 注销事件
			self.unbindEvents(); # 绑定事件
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent = None, params = {}):
		# 创建视图UI类
		windowPos = (0,0);
		windowSize = _GG("AppConfig")["AppSize"];
		if "windowSize" in params:
			windowSize = params["windowSize"];
		windowStyle = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.CAPTION); # wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.CLOSE_BOX);
		self.__ui = MainWindowUI(parent, id = -1, pos = windowPos, size = windowSize, style = windowStyle, curPath = self._curPath, windowCtr = self);
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

	def bindEvents(self):
		_GG("WindowObject").ParentWindowCtr.bindEventToClientWinSize(self, self.onClientWinSize);
		self.initToolWinSizeEvents();

	def unbindEvents(self):
		_GG("WindowObject").ParentWindowCtr.unbindEventToClientWinSize(self);

	def onClientWinSize(self, event):
		PreUISize = _GG("WindowObject").ParentWindowCtr.PreUISize;
		parentWindowUI = _GG("WindowObject").ParentWindowCtr.getUI();
		curSize = parentWindowUI.GetSize();
		self.__ui.Size = (self.__ui.Size[0] + curSize[0] - PreUISize[0], self.__ui.Size[1] + curSize[1] - PreUISize[1]);

	def createHomePage(self):
		itemPageData = self.getCtrByKey("WindowLeftViewCtr").getFirstItemPageData();
		if itemPageData:
			# 先销毁后创建
			self.getCtrByKey("WindowRightViewCtr").destroyPageByPageKey(itemPageData);
			self.getCtrByKey("WindowRightViewCtr").createPageToNoteBook(itemPageData);

	def getToolWinSize(self):
		noteBookSize = self.getCtrByKey("WindowRightViewCtr").getUIByKey("NoteBookViewCtr").GetSize();
		return (noteBookSize[0] - 8, noteBookSize[1] - 30);

	def initToolWinSizeEvents(self):
		self.getCtrByKey("WindowRightViewCtr").getUIByKey("NoteBookViewCtr").Bind(wx.EVT_SIZE, self.onToolWinSize);

	def bindEventToToolWinSize(self, obj, func):
		if callable(func):
			objId = id(obj);
			if objId not in self.toolWinSizeEventDict:
				self.toolWinSizeEventDict[objId] = {"obj" : obj, "funcDict" : {}};
			self.toolWinSizeEventDict[objId]["funcDict"][id(func)] = func;

	def unbindEventToToolWinSize(self, obj, func = None):
		objId = id(obj);
		if objId in self.toolWinSizeEventDict:
			if not func:
				self.toolWinSizeEventDict.pop(objId);
			elif callable(func):
				funcId = id(func);
				if funcId in self.toolWinSizeEventDict[objId]["funcDict"]:
					self.toolWinSizeEventDict[objId]["funcDict"].pop(funcId);

	def onToolWinSize(self, event):
		if not hasattr(self, "OriToolUISize"):
			self.OriToolUISize = self.getCtrByKey("WindowRightViewCtr").getUIByKey("NoteBookViewCtr").GetSize();
			self.PreToolUISize = self.getCtrByKey("WindowRightViewCtr").getUIByKey("NoteBookViewCtr").GetSize();
		curToolUISize = self.getCtrByKey("WindowRightViewCtr").getUIByKey("NoteBookViewCtr").GetSize();
		sizeInfo = {
			"oriDiff" : curToolUISize - self.OriToolUISize,
			"preDiff" : curToolUISize - self.PreToolUISize,
		}
		for objId in self.toolWinSizeEventDict:
			if self.toolWinSizeEventDict[objId]["obj"]:
				for funcId in self.toolWinSizeEventDict[objId]["funcDict"]:
					self.toolWinSizeEventDict[objId]["funcDict"][funcId](sizeInfo, event = event);
		# 重置PreToolUISize
		self.PreToolUISize = curToolUISize;

	def getMainWindowCenterPoint(self, isToScreen = True):
		pos = self.__ui.GetPosition();
		if isToScreen == True:
			pos = self.__ui.ClientToScreen(pos);
		return wx.Point(pos[0] + self.__ui.GetSize().x/2, pos[1] + self.__ui.GetSize().y/2);

	def checkTreeItemKey(self, itemKey):
		return self.getCtrByKey("WindowLeftViewCtr").checkItemKey(itemKey);
		
	def getItemDataByKey(self, itemKey):
		return self.getCtrByKey("WindowLeftViewCtr").getItemData(itemKey);