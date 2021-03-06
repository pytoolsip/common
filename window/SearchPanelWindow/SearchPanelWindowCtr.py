# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-05 21:14:16
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-03 22:15:09

import wx;

from _Global import _GG;
from _Global import isExist_G;
from function.threadEx import stopThread;

from SearchPanelWindowUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateWindow",
	};

class SearchPanelWindowCtr(object):
	"""docstring for SearchPanelWindowCtr"""
	def __init__(self, parent = None, params = {}):
		super(SearchPanelWindowCtr, self).__init__();
		self._className_ = SearchPanelWindowCtr.__name__;
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
		windowTitle = "搜索面板";
		windowSize = (380,320); # _GG("AppConfig")["AppSize"];
		windowStyle = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.CAPTION);
		self.__ui = SearchPanelWindowUI(parent, id = -1, title = windowTitle, size = windowSize, style = windowStyle, curPath = self._curPath, windowCtr = self);
		self.__ui.SetBackgroundColour(wx.Colour(210,210,210));
		self.__ui.initWindow();

	def getUI(self, parent = None):
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

	def clearWindow(self):
		self.__ui.clearWindow();

	def getCenterPosByParentSize(self, pSize):
		sSize = self.__ui.GetSize();
		return (pSize[0]/2 - sSize[0]/2), (pSize[1]/2 - sSize[1]/2);

	# 搜索文本回调
	def onSearchText(self, event):
		if hasattr(self, "searchThread"):
			stopThread(self.searchThread);
		self.searchThread = threading.Thread(target = self.onSearchTextByNewThread, args = ({"searchText" : event.GetString()},));
		self.searchThread.start();

	def onSearchTextByNewThread(self, data):
		searchText = "";
		if "searchText" in data:
			searchText = data["searchText"];
		searchData = self.getSearchPanelData(searchText);
		wx.CallAfter(self.getCtrByKey("SearchPanelViewCtr").updateView, searchData);

	def getSearchPanelData(self, searchText = ""):
		searchData = [];
		if searchText != "":
			mainWinLeftViewCtr = _GG("WindowObject").MainWindowCtr.getCtrByKey("WindowLeftViewCtr");
			treeItemsViewCtr = mainWinLeftViewCtr.getCtrByKey("TreeItemsViewCtr");
			for v in treeItemsViewCtr.itemPageDataDict.values():
				if "title" in v and v["title"].find(searchText) >= 0:
					searchData.append(self.convertSearchData(v));
		return searchData;

	def convertSearchData(self, data):
		toolPath = data["title"];
		if data["category"]:
			toolPath = "/".join([data["category"], data["title"]])
		return {
			"name" : data["title"],
			"path" : toolPath,
			"key" : data["key"],
			"pagePath" : data["pagePath"],
			"category" : data["category"],
		};