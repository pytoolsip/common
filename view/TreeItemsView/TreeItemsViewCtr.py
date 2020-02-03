# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 17:27:44
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-03 21:54:23

import wx;
from enum import Enum, unique;

from _Global import _GG;

from TreeItemsViewUI import *;

# Item类型
@unique
class ItemType(Enum):
	Tool = 0;
	Catalog = 1;

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.UPDATE_TREE_ITEMS : "updateView",
	};

class TreeItemsViewCtr(object):
	"""docstring for TreeItemsViewCtr"""
	def __init__(self, parent, params = {}):
		super(TreeItemsViewCtr, self).__init__();
		self._className_ = TreeItemsViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.initParams(params); # 初始化相关参数/属性
		self.initPopupMenus(); # 创建弹出菜单
		self.getUI().createTreeItems(params.get("itemsData", [])); # 创建树

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
		self.__ui = TreeItemsViewUI(parent, curPath = self._curPath, viewCtr = self);
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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/ToolServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		# 判断要更新视图的类型ID
		if self.__type and ("type" in data):
			if data["type"] != self.__type:
				return; # 若不需要更新当前视图，则直接返回，不执行更新逻辑
		self.getUI().updateView(data);

	def initParams(self, params):
		# 树节点的页面数据字典
		self.__itemPageDataDict = {};
		# 用于标记当前类的类型ID
		self.__type = params.get("type", None);
		# 选中树节点的回调函数
		self.__onActivated = params.get("onActivated", None);
		# 添加树节点的回调函数
		self.__onAddItem = params.get("onAddItem", None);
		# 移除树节点的回调函数
		self.__onRemoveItem = params.get("onRemoveItem", None);
		# 初始化弹出菜单的节点
		self.__popupMenuItem = None;
		pass;

	@property
	def itemPageDataDict(self):
		return self.__itemPageDataDict;

	def bindEventToItem(self, item, itemInfo, pathList):
		if "key" in itemInfo:
			basePath = _GG(itemInfo["trunk"]);
			if "branch" in itemInfo:
				basePath += itemInfo["branch"] + "/";
			self.__itemPageDataDict[item] = {
				"item" : item,
				"key" : itemInfo["key"],
				"pagePath" : (basePath + itemInfo["path"]).replace("/", "/"),
				"category" : "/".join(pathList),
				"title" : itemInfo.get("title", itemInfo["name"]),
				"description" : itemInfo.get("description", ""),
				"version" : itemInfo.get("version", ""),
				"author" : itemInfo.get("author", ""),
			};
		pass;

	def onActivated(self, event):
		item = event.GetItem();
		if item in self.__itemPageDataDict and callable(self.__onActivated):
			self.__onActivated(self.__itemPageDataDict[item]);

	def onMouseRightDown(self, event):
		UI = self.getUI();
		item, flags = UI.HitTest(event.GetPosition());
		if item.IsOk() and flags == wx.TREE_HITTEST_ONITEMLABEL:
			UI.SelectItem(item);
			self.showPopupMenu(item, event.GetPosition());
		pass;

	def getItemPageData(self, itemKey):
		for pageData in self.__itemPageDataDict.values():
			if pageData["key"] == itemKey:
				return pageData;
		return {};

	def getItem(self, itemKey):
		pageData = self.getItemPageData(itemKey);
		return pageData.get("item", None);

	def addItem(self, nameList, itemInfo):
		item = self.getUI().checkTreeItem(nameList);
		self.bindEventToItem(item, itemInfo, nameList[:-1]);
		self.getUI().SelectItem(item);
		if callable(self.__onAddItem):
			self.__onAddItem(self.__itemPageDataDict[item], itemInfo);

	def removeItem(self, itemKey):
		item = self.getItem(itemKey);
		if item:
			itemText = self.getUI().GetItemText(item);
			pageData = self.__itemPageDataDict.pop(item);
			self.getUI().removeTreeItem(item);
			if callable(self.__onRemoveItem):
				self.__onRemoveItem(pageData, itemText);

	def initPopupMenus(self):
		self.getCtrByKey("PopupMenuViewCtr").createNewMenu(ItemType.Tool, {"itemsData" : self.getToolPopupMenuItemsData()});
		self.getCtrByKey("PopupMenuViewCtr").createNewMenu(ItemType.Catalog, {"itemsData" : self.getCatalogPopupMenuItemsData()});

	def showPopupMenu(self, item, pos):
		self.__popupMenuItem = item;
		if item in self.__itemPageDataDict:
			if not self.__itemPageDataDict[item]["category"]:
				return;
			self.getUI().PopupMenu(self.getCtrByKey("PopupMenuViewCtr").getMenu(ItemType.Tool), pos);
		else:
			self.getUI().PopupMenu(self.getCtrByKey("PopupMenuViewCtr").getMenu(ItemType.Catalog), pos);

	def showMessageDialog(self, message, caption = "删除工具", style = wx.YES_NO|wx.ICON_EXCLAMATION):
		return wx.MessageDialog(self.getUI(), message, caption = caption, style = style).ShowModal();

	def onDeleteItem(self, event):
		if not self.__popupMenuItem:
			return;
		itemText = self.getUI().GetItemText(self.__popupMenuItem);
		itemData = self.__itemPageDataDict.get(self.__popupMenuItem, None);
		if itemData:
			if not itemData["category"]:
				self.showMessageDialog("不能删除该工具【%s】！"%itemText);
				return;
			if self.showMessageDialog("是否确认删除工具【%s】？"%(itemData["category"]+"/"+itemText)) == wx.ID_YES:
				self.removeItem(itemData["key"]);
		else:
			itemDataList = self.getItemDataListByItem(self.__popupMenuItem);
			if len(itemDataList) == 0:
				return;
			idx = itemDataList[0]["category"].find(itemText);
			if idx == -1:
				_GG("Log").w("There is not text[%s] in category[%s]！"%(itemText, itemDataList[0]["category"]));
				return;
			category = itemDataList[0]["category"][:idx] + itemText;
			toolNamePathList = [];
			for itemData in itemDataList:
				toolNamePathList.append("/".join([itemData["category"][itemData["category"].find(itemText):], itemData["title"]]));
			if self.showMessageDialog("是否确认删除分类【%s】？\n该分类包含工具：\n%s"%(category, "/".join(toolNamePathList))) == wx.ID_YES:
				for itemData in itemDataList:
					self.removeItem(itemData["key"]);

	def getItemDataListByItem(self, item, itemDataList = []):
		UI = self.getUI();
		item, cookie = UI.GetFirstChild(item);
		while item.IsOk():
			if item in self.__itemPageDataDict:
				itemDataList.append(self.__itemPageDataDict[item]);
			self.getItemDataListByItem(item, itemDataList = itemDataList);
			item, cookie = UI.GetNextChild(item, cookie);
		return itemDataList;

	def onShowToolInfo(self, event):
		if not self.__popupMenuItem:
			return;
		itemText = self.getUI().GetItemText(self.__popupMenuItem);
		itemData = self.__itemPageDataDict.get(self.__popupMenuItem, None);
		if itemData:
			self._showToolInfo_({
				"name" : itemText,
				"path" : itemData["category"],
				"author" : itemData["author"],
				"version" : itemData["version"],
				"description" : {
					"value" : itemData["description"],
				},
				"download" : {},
			});
		else:
			self.showMessageDialog("显示工具【%s】信息失败！"%itemText);

	def getToolPopupMenuItemsData(self):
		return [
			{
				"title" : "删除工具",
				"callback" : self.onDeleteItem,
			},
			{
				"title" : "显示工具信息",
				"callback" : self.onShowToolInfo,
			},
		];

	def getCatalogPopupMenuItemsData(self):
		return [
			{
				"title" : "删除分类",
				"callback" : self.onDeleteItem,
			},
		];