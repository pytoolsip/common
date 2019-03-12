# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 18:27:07
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-12 17:42:41

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
		self.className_ = NoteBookViewCtr.__name__;
		self.curPath = _GG("g_CommonPath") + "view\\NoteBookView\\";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件

		self.pageInfoDict = {}; # 页面信息字典
		self.relievedPageId = -1; # 已释放页面Id
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
		self.UI = NoteBookViewUI(parent, curPath = self.curPath, viewCtr = self);
		self.UI.initView();
		self.UI.Bind(wx.EVT_RIGHT_DOWN, self.onMouseRightDown);

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

	def initPopupMenus(self):
		self.createNewMenu(PageType.Fix, {"itemsData" : self.getFixedPopupMenuItemsData()});
		self.createNewMenu(PageType.Relieve, {"itemsData" : self.getRelievedPopupMenuItemsData()});
		pass;

	def createNewMenu(self, key, data):
		self.getCtrByKey("PopupMenuViewCtr").createNewMenu(key, data);
		pass;

	def resetData(self, pageId = -1):
		if pageId == -1:
			self.pageInfoDict = {};
			self.relievedPageId = -1;
		else:
			if pageId in self.pageInfoDict:
				pageInfo = self.pageInfoDict.pop(pageId);
				DelCtr(pageInfo["pageViewCtr"]); # 销毁页面视图控制类
			if self.relievedPageId == pageId:
				self.relievedPageId = -1;
		pass;

	def setCurrentPageInt(self, curPageInt):
		self.UI.SetSelection(curPageInt);
		pass;

	def getCurrentPageInt(self):
		return self.UI.GetSelection();

	def getCurrentPage(self):
		return self.UI.GetCurrentPage();

	def createPageViewCtr(self, path):
		return CreateCtr(path, self.UI);

	def addPageToNoteBook(self, pageId = -1, pageInfo = None):
		if not pageInfo:
			pageInfo = self.pageInfoDict[pageId];
		return self.UI.addPage(pageInfo["pageViewCtr"].getUI(), pageInfo["title"]);

	def setPageTitle(self, pageId, pageInt):
		pageInfo = self.pageInfoDict[pageId];
		return self.UI.SetPageText(pageInt, pageInfo["title"]);

	def adjustPageTitle(self, pageId = -1, pageInfo = None):
		if not pageInfo:
			pageInfo = self.pageInfoDict[pageId];
		isRelieveTitle = pageInfo["title"][-1] == "*";
		if isRelieveTitle:
			if pageInfo["pageType"] == PageType.Fix:
				pageInfo["title"] = pageInfo["title"][0:-2];
		else:
			if pageInfo["pageType"] == PageType.Relieve:
				pageInfo["title"] = pageInfo["title"] + " *";
		pass;

	def checkRelievedPageId(self, isDeleteOldPage = False):
		if self.relievedPageId == -1:
			return True;
		elif isDeleteOldPage:
			pageInfo = self.pageInfoDict[self.relievedPageId];
			UI = self.getUI();
			if UI.DeletePage(UI.FindPage(pageInfo["pageViewCtr"].getUI())):
				self.resetData(self.relievedPageId);
			return True;
		return False;

	def createPageToNoteBook(self, pageId, path, title):
		if pageId not in self.pageInfoDict:
			pageViewCtr = self.createPageViewCtr(path);
			pageViewCtr.getUI().SetId(pageId);
			pageInfo = {"pageViewCtr" : pageViewCtr, "pageType" : PageType.Relieve, "title" : title};
			self.adjustPageTitle(pageInfo = pageInfo);
			pageInt = self.addPageToNoteBook(pageInfo = pageInfo);
			self.setCurrentPageInt(pageInt);
			if self.checkRelievedPageId(isDeleteOldPage = True):
				self.relievedPageId = pageId;
			self.pageInfoDict[pageId] = pageInfo;
			return True;
		else:
			pageInfo = self.pageInfoDict[pageId];
			page = pageInfo["pageViewCtr"].getUI();
			self.setCurrentPageInt(self.getUI().FindPage(page));
			return False;

	def onMouseRightDown(self, event):
		UI = self.getUI();
		pageIndexs = UI.HitTest(event.GetPosition());
		self.setCurrentPageInt(pageIndexs[0]);
		popupMenu = self.getPopupMenu(UI.GetPage(pageIndexs[0]).GetId());
		if popupMenu:
			UI.PopupMenu(popupMenu, event.GetPosition());
		pass;
		
	def getPopupMenu(self, pageId = None):
		if pageId in self.pageInfoDict:
			pageType = self.pageInfoDict[pageId]["pageType"];
			return self.getCtrByKey("PopupMenuViewCtr").getMenu(pageType);

	def onFixCurPage(self, event):
		curPageId = self.getCurrentPage().GetId();
		if self.relievedPageId == curPageId:
			self.pageInfoDict[curPageId]["pageType"] = PageType.Fix;
			self.adjustPageTitle(curPageId);
			self.setPageTitle(curPageId, self.getCurrentPageInt());
			self.relievedPageId = -1;
		pass;

	def onRelieveCurPage(self, event):
		curPageId = self.getCurrentPage().GetId();
		if self.checkRelievedPageId(isDeleteOldPage = True):
			self.pageInfoDict[curPageId]["pageType"] = PageType.Relieve;
			self.adjustPageTitle(curPageId);
			self.setPageTitle(curPageId, self.getCurrentPageInt());
			self.relievedPageId = curPageId;
		pass;

	def onCloseCurPage(self, event):
		curPageId = self.getCurrentPage().GetId();
		curPageInt = self.getCurrentPageInt();
		UI = self.getUI();
		if UI.DeletePage(curPageInt):
			self.resetData(curPageId);
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