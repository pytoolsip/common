# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-11 23:20:11

import wx;

from _Global import _GG;

from HomePageViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class HomePageViewCtr(object):
	"""docstring for HomePageViewCtr"""
	def __init__(self, parent, params = {}):
		super(HomePageViewCtr, self).__init__();
		self.className_ = HomePageViewCtr.__name__;
		self.curPath = _GG("g_CommonPath") + "view\\HomePageView\\";
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
		self.UI = HomePageViewUI(parent, curPath = self.curPath, viewCtr = self, params = params);
		self.UI.initView();

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

	def updateRankingPagesView(self):
		self.getCtrByKey("RankingPagesViewCtr").addDownPage(_GG("g_CommonPath") + "view\\RankingListView",
		 "popularity", "人气", params = {"size" : (self.UI.getRankingSizeX(), self.UI.GetSize()[1])});
		self.getCtrByKey("RankingPagesViewCtr").addDownPage(_GG("g_CommonPath") + "view\\RankingListView",
		 "praise", "好评", params = {"size" : (self.UI.getRankingSizeX(), self.UI.GetSize()[1])});
		self.getCtrByKey("RankingPagesViewCtr").addDownPage(_GG("g_CommonPath") + "view\\RankingListView",
		 "download", "下载", params = {"size" : (self.UI.getRankingSizeX(), self.UI.GetSize()[1])});
		self.updateRankingPage();

	def updateRankingPage(self):
		self.getUIByKey("RankingPagesViewCtr").pageDict["popularity"].getCtr().updateViewByDefaultData();
		self.getUIByKey("RankingPagesViewCtr").pageDict["praise"].getCtr().updateViewByDefaultData();
		self.getUIByKey("RankingPagesViewCtr").pageDict["download"].getCtr().updateViewByDefaultData();

	# 请求工具信息列表的回调
	def onRequestToolInfos(self, retData):
		if not retData or not retData.isSuccess:
			return;
		# 处理返回的工具信息列表
		infos = _GG("CommonClient").decodeBytes(retData.data);
		gridsData = [];
		for info in infos:
			gridsData.append({
				"title" : info["title"],
				"version" : info["version"],
				"detail" : info["detail"],
				"name" : info["userName"],
			});
		self.getCtrByKey("NewestGridsViewCtr").updateView({"gridsData" : gridsData});
		self.getCtrByKey("RecommendToolsCtr").updateView({"gridsData" : gridsData});

	def callService(self):
		# 请求工具信息列表
		_GG("CommonClient").callService("Request", "Req", {
			"key" : "RequestToolInfos",
			"data" : _GG("CommonClient").encodeBytes({"commonVersion" : _GG("AppConfig")["version"]}),
		}, asynCallback = self.onRequestToolInfos);