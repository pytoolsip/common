# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-11 23:19:38

import wx;

from _Global import _GG;
from function.base import *;

class HomePageViewUI(wx.ScrolledWindow):
	"""docstring for HomePageViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(HomePageViewUI, self).__init__(parent, id, size = self.__params["size"]);
		self.className_ = HomePageViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.bindEvents(); # 绑定事件
		# 初始化滚动条参数
		self.SetScrollbars(1, 1, *self.__params["size"]);

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unbindEvents();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : _GG("WindowObject").GetToolWinSize(),
			"rankingSizeX" : 250,
			"bgColor" : wx.Colour(250,250,250),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.viewCtr;

	def bindEvents(self):
		_GG("WindowObject").BindEventToToolWinSize(self, self.onToolWinSize);

	def unbindEvents(self):
		_GG("WindowObject").UnbindEventToToolWinSize(self);

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.SetBackgroundColour(self.__params["bgColor"]); # 设置背景颜色
		self.getCtr().updateRankingPagesView();

	def createControls(self):
		# 创建推荐视图
		self.getCtr().createCtrByKey("RecommendToolsCtr", _GG("g_CommonPath") + "view\\TitleGridsView",
		 params = {"size" : (self.GetSize()[0] - self.__params["rankingSizeX"], self.GetSize()[1]), "title" : "推荐工具"});
		# 创建排行榜
		self.getCtr().createCtrByKey("RankingPagesViewCtr", _GG("g_CommonPath") + "view\\DownPagesView",
		 params = {"size" : (self.__params["rankingSizeX"], self.GetSize()[1]), "title" : "排行榜"});
		# 创建最新视图
		self.getCtr().createCtrByKey("NewestGridsViewCtr", _GG("g_CommonPath") + "view\\PageGridsView",
		 params = {"size" : (self.GetSize()[0], self.GetSize()[1]*2/3), "title" : "最新工具"});
		pass;
		
	def initViewLayout(self):
		gridBagSizer = wx.GridBagSizer(0,0);
		gridBagSizer.Add(self.getCtr().getUIByKey("RecommendToolsCtr"), pos = (1,1), span = (1,1), flag = wx.EXPAND);
		gridBagSizer.Add(self.getCtr().getUIByKey("RankingPagesViewCtr"), pos = (1,2), span = (1,1), flag = wx.LEFT|wx.RIGHT, border = 6);
		gridBagSizer.Add(self.getCtr().getUIByKey("NewestGridsViewCtr"), pos = (2,1), span = (1,2), flag = wx.EXPAND|wx.TOP, border = 10);
		gridBagSizer.AddGrowableCol(1)
		self.SetSizerAndFit(gridBagSizer);
		pass;

	def updateView(self, data):
		pass;

	def getRankingSizeX(self):
		return self.__params["rankingSizeX"];

	def onToolWinSize(self, sizeInfo, event = None):
		self.SetSize(self.GetSize() + sizeInfo["preDiff"]);
		# 获取变化的大小
		diffSize = self.GetSize() - self.GetBestSize();
		diffSize = wx.Size(max(0, diffSize.x), max(0, diffSize.y));
		self.getCtr().getUIByKey("RecommendToolsCtr").layoutView(diffSize);
		self.getCtr().getUIByKey("RankingPagesViewCtr").Refresh();
		self.getCtr().getUIByKey("NewestGridsViewCtr").layoutView(diffSize)
		self.Layout()
		pass;