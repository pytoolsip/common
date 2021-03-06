# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 14:46:20
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-06 20:21:34

import wx, os, shutil;
import threading;

from _Global import _GG;

from WindowLeftViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.LOGIN_SUCCESS_EVENT : "updateUserNameView",
		G_EVENT.UPDATE_WINDOW_LEFT_VIEW : "updateTreeView",
		G_EVENT.LOGOUT_SUCCESS_EVENT : "resetUserNameView",
		G_EVENT.SAVE_FIXED_PAGE_DATA : "saveFixedPageData",
		G_EVENT.REVEAL_IN_WINDOW_LEFT_VIEW : "selectPageItem",
	};

class WindowLeftViewCtr(object):
	"""docstring for WindowLeftViewCtr"""
	def __init__(self, parent, params = {}):
		super(WindowLeftViewCtr, self).__init__();
		self._className_ = WindowLeftViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.initTreeItemsData(); # 初始化树节点数据
		self.initUI(parent); # 初始化视图UI
		wx.CallAfter(self.initFixedPage); # 初始化固定标签页

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
		self.__ui = WindowLeftViewUI(parent, curPath = self._curPath, viewCtr = self);
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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "ConfigParseBehavior/JsonConfigBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/UserServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		_GG("BehaviorManager").bindBehavior(self, {"path" : "verifyBehavior/VerifyDependsBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.__ui.updateView(data);

	def initTreeItemsData(self):
		self.__treeItemsData = [];
		if os.path.exists(_GG("g_DataPath")+"config/tools_tree.json"):
			self.__treeItemsData = self.readJsonFile(_GG("g_DataPath")+"config/tools_tree.json");

	def saveTreeItemsData(self):
		self.writeJsonFile(_GG("g_DataPath")+"config/tools_tree.json", self.__treeItemsData);

	def updateUserNameView(self, data):
		def onClick(event):
			# 显示玩家信息的弹窗
			pass;
		self.getCtrByKey("UserNameTextViewCtr").updateView({"name" : data["userInfo"].name, "onClick" : onClick});

	def resetUserNameView(self, data):
		self.getCtrByKey("UserNameTextViewCtr").updateView({"name" : "点击登录", "onClick" : self.onClickLogin});

	def onClickLogin(self, event):
		self._loginIP_();

	# 创建树控件
	def createTreeCtrl(self):
		def onActivated(pageInfo):
			if self._checkDependMods_(os.path.dirname(pageInfo["pagePath"])):
				_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_WINDOW_RIGHT_VIEW, {
					"createPage" : True,
					"key" : pageInfo["key"],
					"pagePath" : pageInfo["pagePath"],
					"category" : pageInfo["category"],
					"title" : pageInfo["title"]
				});
			pass;
		def onAddItem(pageInfo, itemInfo):
			itemData = self.checkTreeItemsData(self.getNameList(pageInfo["category"], itemInfo["name"]), self.__treeItemsData);
			for key in ["key", "name", "trunk", "branch", "path", "description", "version", "author"]:
				itemData[key] = itemInfo.get(key, "");
			self.saveTreeItemsData();
			pass;
		def onRemoveItem(pageInfo, name):
			self.checkTreeItemsData(self.getNameList(pageInfo["category"], name), self.__treeItemsData, exData = {"isRemove" : True});
			self.saveTreeItemsData();
			_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_WINDOW_RIGHT_VIEW, {
				"destroyPage" : True,
				"key" : pageInfo["key"],
			});
			assetsPath = os.path.dirname(os.path.dirname(pageInfo["pagePath"])); # 中间还有一层tool
			# 移除依赖模块
			proDialog = wx.ProgressDialog("卸载依赖模块", "", style = wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME|wx.PD_ESTIMATED_TIME|wx.PD_REMAINING_TIME|wx.PD_AUTO_HIDE);
			def onUninstall(mod, value, isEnd = False):
				if not isEnd:
					wx.CallAfter(proDialog.Update, value, f"正在卸载模块【{mod}】...");
				else:
					wx.CallAfter(proDialog.Update, value, f"成功卸载模块【{mod}】。");
				pass;
			def onFinish():
				# 移除工具文件夹
				if os.path.exists(assetsPath):
					shutil.rmtree(assetsPath);
				wx.CallAfter(proDialog.Update, 1, f"完成依赖模块的卸载。");
			threading.Thread(target = self._uninstallDependMods_, args = (pageInfo["key"], assetsPath+"/tool", _GG("g_PythonPath"), onUninstall, onFinish)).start();
			proDialog.Update(0, "开始卸载依赖模块...");
			proDialog.ShowModal();
			pass;
		self.createCtrByKey("TreeItemsViewCtr", _GG("g_CommonPath") + "view/TreeItemsView", parent = self.getUI(), params = {
			"itemsData" : self.__treeItemsData,
			"type" : "WINDOW_LEFT_TREE",
			"onActivated" : onActivated,
			"onAddItem" : onAddItem,
			"onRemoveItem" : onRemoveItem,
		});

	def getFirstItemData(self):
		if len(self.__treeItemsData) > 0:
			return self.__treeItemsData[0];
		return {};

	def getFirstItemPageData(self):
		itemData = self.getFirstItemData();
		return self.getCtrByKey("TreeItemsViewCtr").getItemPageData(itemData.get("key", ""));

	def getNameList(self, category, name, nameList = []):
		if category:
			nameList = category.split("/");
		nameList.append(name);
		return nameList;

	def checkTreeItemsData(self, nameList, treeItemsData, exData = {}):
		exData["__isRemoveChild"] = False; # 重置标记
		name = nameList.pop(0);
		for i in range(len(treeItemsData)):
			itemData = treeItemsData[i];
			if itemData["name"] == name:
				if len(nameList) == 0:
					if exData.get("isRemove", False):
						treeItemsData.pop(i);
						exData["__isRemoveChild"] = True;
					return itemData;
				else:
					if "items" not in itemData:
						itemData["items"] = [];
					result = self.checkTreeItemsData(nameList, itemData["items"], exData = exData);
					if exData.get("__isRemoveChild", False):
						if len(itemData["items"]) <= 1:
							treeItemsData.pop(i);
						else:
							exData["__isRemoveChild"] = False;
					return result;
			pass;
		if exData.get("isRemove", False):
			return {};
		# 添加新节点
		newItemData = {"name" : name};
		treeItemsData.append(newItemData);
		if len(nameList) == 0:
			return newItemData;
		else:
			newItemData["items"] = [];
			return self.checkTreeItemsData(nameList, newItemData["items"], exData = exData);

	def updateTreeView(self, data):
		if "key" not in data or "name" not in data:
			return;
		action = data.get("action", "add");
		if action == "add":
			nameList = [];
			if data.get("category", None):
				if data["category"][-1] == "/":
					nameList = data["category"][:-1].split("/");
				else:
					nameList = data["category"].split("/");
			nameList.append(data["name"]);
			itemData = {"name" : data["name"]};
			for key in ["key", "name", "trunk", "branch", "path", "description", "version", "author"]:
				itemData[key] = data.get(key, "");
			self.getCtrByKey("TreeItemsViewCtr").addItem(nameList, itemData);
		if action == "remove":
			self.getCtrByKey("TreeItemsViewCtr").removeItem(data["key"]);

	def checkItemKey(self, itemKey):
		return self.getCtrByKey("TreeItemsViewCtr").getItem(itemKey) != None;
		
	def getItemData(self, itemKey):
		return self.getCtrByKey("TreeItemsViewCtr").getItemPageData(itemKey);

	def saveFixedPageData(self, data):
		if "pageKeyList" in data:
			self.writeJsonFile(_GG("g_DataPath")+"config/fixed_page_key_list.json", data["pageKeyList"]);
		pass;

	def initFixedPage(self):
		pageKeyList = [];
		if os.path.exists(_GG("g_DataPath")+"config/fixed_page_key_list.json"):
			pageKeyList = self.readJsonFile(_GG("g_DataPath")+"config/fixed_page_key_list.json");
		if pageKeyList:
			pageDataList = [];
			for key in pageKeyList:
				pageData = self.getCtrByKey("TreeItemsViewCtr").getItemPageData(key);
				if pageData:
					pageDataList.append(pageData);
			_GG("EventDispatcher").dispatch(_GG("EVENT_ID").CREATE_FIXED_PAGE, {
				"pageDataList" : pageDataList,
			});
		pass;
	
	def selectPageItem(self, data):
		if "curPageKey" in data:
			self.getCtrByKey("TreeItemsViewCtr").selectItem(data["curPageKey"]);