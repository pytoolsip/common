# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-03 10:49:14

import wx;

from _Global import _GG;
from function.base import *;

from HomePageViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class HomePageViewCtr(object):
	"""docstring for HomePageViewCtr"""
	def __init__(self, parent, params = {}):
		super(HomePageViewCtr, self).__init__();
		self._className_ = HomePageViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.callService(); # 调用服务

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
		self.__ui = HomePageViewUI(parent, curPath = self._curPath, viewCtr = self, params = params);
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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/ToolServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.__ui.updateView(data);

	def updateRankingPagesView(self):
		self.getCtrByKey("RankingPagesViewCtr").addDownPage(_GG("g_CommonPath") + "view/RankingListView",
		 "popularity", "人气", params = {"size" : (self.__ui.getRankingSizeX(), self.__ui.GetSize()[1])});
		self.getCtrByKey("RankingPagesViewCtr").addDownPage(_GG("g_CommonPath") + "view/RankingListView",
		 "praise", "好评", params = {"size" : (self.__ui.getRankingSizeX(), self.__ui.GetSize()[1])});
		self.getCtrByKey("RankingPagesViewCtr").addDownPage(_GG("g_CommonPath") + "view/RankingListView",
		 "download", "下载", params = {"size" : (self.__ui.getRankingSizeX(), self.__ui.GetSize()[1])});

	def getListData(self, toolInfos, onClickItem, numFunc):
		listData, index = [], 0;
		for info in toolInfos:
			index += 1;
			listData.append({
				"index" : index,
				"num" : numFunc(info),
				"title" : info.name,
				"detail" : info.author,
				"toolInfo" : {
					"key" : info.tkey,
					"title" : info.name,
					"category" : info.category,
					"description" : info.description,
					"version" : info.version,
					"author" : info.author,
				},
				"onClick" : onClickItem,
			});
		return listData;

	def updateRankingPage(self, toolInfos, onClickItem):
		def popularity(toolInfo):
			return toolInfo.download * toolInfo.score;
		self.getUIByKey("RankingPagesViewCtr").pageDict["popularity"].getCtr().updateView({"listData" : self.getListData(toolInfos, onClickItem, popularity)});
		def download(toolInfo):
			return toolInfo.download;
		self.getUIByKey("RankingPagesViewCtr").pageDict["download"].getCtr().updateView({"listData" : self.getListData(toolInfos, onClickItem, download)});
		def score(toolInfo):
			return toolInfo.download;
		self.getUIByKey("RankingPagesViewCtr").pageDict["praise"].getCtr().updateView({"listData" : self.getListData(toolInfos, onClickItem, score)});

	# 请求工具信息列表的回调
	def onRequestToolInfos(self, retData):
		if not retData or retData.code != 0:
			return;
		def onClickItem(item, itemData):
			toolInfo = itemData["toolInfo"];
			self._showToolInfo_({
				"key" : toolInfo["key"],
				"name" : toolInfo.get("title", ""),
				"path" : toolInfo.get("category", ""),
				"version" : toolInfo.get("version", ""),
				"author" : toolInfo.get("author", ""),
				"description" : {
					"value" : toolInfo.get("description", ""),
				},
			});
		# 处理返回的工具信息列表
		infos = retData.toolList;
		gridsData = [];
		for info in infos:
			gridsData.append({
				"title" : info.name,
				"version" : info.version,
				"detail" : info.description,
				"name" : info.author,
				"toolInfo" : {
					"key" : info.tkey,
					"title" : info.name,
					"category" : info.category,
					"description" : info.description,
					"version" : info.version,
					"author" : info.author,
				},
				"onClick" : onClickItem,
			});
		self.getCtrByKey("NewestGridsViewCtr").updateView({"gridsData" : gridsData});
		self.getCtrByKey("RecommendToolsCtr").updateView({"gridsData" : gridsData});
		self.updateRankingPage(infos, onClickItem);
		# 更新大小
		self.getUI().onToolWinSize();

	def callService(self):
		# 请求工具信息列表
		_GG("CommonClient").callService("ReqToolInfo", "ToolReq", {
			"IPBaseVer" : GetBaseVersion(_GG("ClientConfig").UrlConfig().GetIPVersion()),
		}, asynCallback = self.onRequestToolInfos);