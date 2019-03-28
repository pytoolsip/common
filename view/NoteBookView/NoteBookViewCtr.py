# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 18:27:07
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-28 19:56:43

from enum import Enum, unique;

import wx;

from _Global import _GG;

from NoteBookViewUI import *;

# 页面类型
@unique
class PageType(Enum):
	Fix = 0;
	Relieve = 1;


def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class NoteBookViewCtr(object):
	"""docstring for NoteBookViewCtr"""
	def __init__(self, parent, params = {}):
		super(NoteBookViewCtr, self).__init__();
		self._className_ = NoteBookViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件

		self.__pageInfoDict = {}; # 页面信息字典
		self.__relievedPageKey = -1; # 已释放页面Id
		self.initPopupMenus(); # 创建弹出菜单

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
		self.__ui = NoteBookViewUI(parent, curPath = self._curPath, viewCtr = self);
		self.__ui.initView();
		self.__ui.Bind(wx.EVT_RIGHT_DOWN, self.onMouseRightDown);

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
		self.__ui.updateView(data);

	def initPopupMenus(self):
		self.createNewMenu(PageType.Fix, {"itemsData" : self.getFixedPopupMenuItemsData()});
		self.createNewMenu(PageType.Relieve, {"itemsData" : self.getRelievedPopupMenuItemsData()});
		pass;

	def createNewMenu(self, key, data):
		self.getCtrByKey("PopupMenuViewCtr").createNewMenu(key, data);
		pass;

	def resetData(self, pageKey = -1):
		if pageKey == -1:
			self.__pageInfoDict = {};
			self.__relievedPageKey = -1;
		else:
			if pageKey in self.__pageInfoDict:
				pageInfo = self.__pageInfoDict.pop(pageKey);
				DelCtr(pageInfo["pageViewCtr"]); # 销毁页面视图控制类
			if self.__relievedPageKey == pageKey:
				self.__relievedPageKey = -1;
		pass;

	def setCurrentPageInt(self, curPageInt):
		self.__ui.SetSelection(curPageInt);
		pass;

	def getCurrentPageInt(self):
		return self.__ui.GetSelection();

	def getCurrentPage(self):
		return self.__ui.GetCurrentPage();

	def getPageKey(self, page):
		if hasattr(page, "_PAGE_KEY"):
			return page._PAGE_KEY;
		return "";

	def setPageKey(self, page, key):
		page._PAGE_KEY = key;

	def createPageViewCtr(self, path):
		return CreateCtr(path, self.__ui);

	def addPageToNoteBook(self, pageKey = -1, pageInfo = None):
		if not pageInfo:
			pageInfo = self.__pageInfoDict[pageKey];
		return self.__ui.addPage(pageInfo["pageViewCtr"].getUI(), pageInfo["title"]);

	def setPageTitle(self, pageKey, pageInt):
		pageInfo = self.__pageInfoDict[pageKey];
		return self.__ui.SetPageText(pageInt, pageInfo["title"]);

	def adjustPageTitle(self, pageKey = -1, pageInfo = None):
		if not pageInfo:
			pageInfo = self.__pageInfoDict[pageKey];
		isRelieveTitle = pageInfo["title"][-1] == "*";
		if isRelieveTitle:
			if pageInfo["pageType"] == PageType.Fix:
				pageInfo["title"] = pageInfo["title"][0:-2];
		else:
			if pageInfo["pageType"] == PageType.Relieve:
				pageInfo["title"] = pageInfo["title"] + " *";
		pass;

	def checkRelievedPageKey(self, isDeleteOldPage = False):
		if self.__relievedPageKey == -1:
			return True;
		elif isDeleteOldPage:
			pageInfo = self.__pageInfoDict[self.__relievedPageKey];
			UI = self.getUI();
			if UI.DeletePage(UI.FindPage(pageInfo["pageViewCtr"].getUI())):
				self.resetData(self.__relievedPageKey);
			return True;
		return False;

	def createPageToNoteBook(self, pageKey, path, title, category):
		if pageKey not in self.__pageInfoDict:
			pageViewCtr = self.createPageViewCtr(path);
			self.setPageKey(pageViewCtr.getUI(), pageKey);
			pageInfo = {"pageViewCtr" : pageViewCtr, "pageType" : PageType.Relieve, "title" : title, "category" : category};
			self.adjustPageTitle(pageInfo = pageInfo);
			pageInt = self.addPageToNoteBook(pageInfo = pageInfo);
			self.setCurrentPageInt(pageInt);
			if self.checkRelievedPageKey(isDeleteOldPage = True):
				self.__relievedPageKey = pageKey;
			self.__pageInfoDict[pageKey] = pageInfo;
			return True;
		else:
			pageInfo = self.__pageInfoDict[pageKey];
			page = pageInfo["pageViewCtr"].getUI();
			self.setCurrentPageInt(self.getUI().FindPage(page));
			return False;

	def onMouseRightDown(self, event):
		UI = self.getUI();
		pageIndexs = UI.HitTest(event.GetPosition());
		self.setCurrentPageInt(pageIndexs[0]);
		popupMenu = self.getPopupMenu(self.getPageKey(UI.GetPage(pageIndexs[0])));
		if popupMenu:
			UI.PopupMenu(popupMenu, event.GetPosition());
		pass;
		
	def getPopupMenu(self, pageKey = None):
		if pageKey in self.__pageInfoDict:
			pageType = self.__pageInfoDict[pageKey]["pageType"];
			return self.getCtrByKey("PopupMenuViewCtr").getMenu(pageType);

	def onFixCurPage(self, event):
		curPageKey = self.getPageKey(self.getCurrentPage());
		if self.__relievedPageKey == curPageKey:
			self.__pageInfoDict[curPageKey]["pageType"] = PageType.Fix;
			self.adjustPageTitle(curPageKey);
			self.setPageTitle(curPageKey, self.getCurrentPageInt());
			self.__relievedPageKey = -1;
		pass;

	def onRelieveCurPage(self, event):
		curPageKey = self.getPageKey(self.getCurrentPage());
		if self.checkRelievedPageKey(isDeleteOldPage = True):
			self.__pageInfoDict[curPageKey]["pageType"] = PageType.Relieve;
			self.adjustPageTitle(curPageKey);
			self.setPageTitle(curPageKey, self.getCurrentPageInt());
			self.__relievedPageKey = curPageKey;
		pass;

	def onCloseCurPage(self, event):
		curPageKey = self.getPageKey(self.getCurrentPage());
		curPageInt = self.getCurrentPageInt();
		UI = self.getUI();
		if UI.DeletePage(curPageInt):
			self.resetData(curPageKey);
		pass;

	def onCloseAllPage(self, event):
		UI = self.getUI();
		UI.DeleteAllPages();
		pass;

	def getFixedPopupMenuItemsData(self):
		return [
			{
				"title" : "释放当前标签页",
				"callback" : self.onRelieveCurPage,
			},
			{
				"title" : "关闭当前标签页",
				"callback" : self.onCloseCurPage,
			},
			{
				"isSeparator" : True,
			},
			{
				"title" : "关闭所有标签页",
				"callback" : self.onCloseAllPage,
			},
		];

	def getRelievedPopupMenuItemsData(self):
		return [
			{
				"title" : "固定当前标签页",
				"callback" : self.onFixCurPage,
			},
			{
				"title" : "关闭当前标签页",
				"callback" : self.onCloseCurPage,
			},
			{
				"isSeparator" : True,
			},
			{
				"title" : "关闭所有标签页",
				"callback" : self.onCloseAllPage,
			},
		];