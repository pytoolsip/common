# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-10 15:59:49
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:03

import wx;

from _Global import _GG;
from function.base import *;
from ui import PageIndexCtrl;
from data import RandomPool;

class PageGridsViewUI(wx.Panel):
	"""docstring for PageGridsViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(PageGridsViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = PageGridsViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__randomPool = RandomPool();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"title" : "标题",
			"antBtnLabel" : "换一批",
			"antBtnSize" : (50,20),
			"itemCols" : 3,
			"itemRows" : 2,
		};
		for k,v in params.items():
			self.__params[k] = v;
		# 校验itemCols和itemRows
		if self.__params["itemCols"] <= 0:
			self.__params["itemCols"] = 1;
		if self.__params["itemRows"] <= 0:
			self.__params["itemRows"] = 1;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.createTitle();
		self.createPageCtrl();
		self.createSketchGridViewCtr();
		
	def initViewLayout(self):
		fGridSizer = wx.FlexGridSizer(1,1,0);
		fGridSizer.Add(self.title, flag = wx.EXPAND|wx.TOP|wx.BOTTOM, border = 4);
		fGridSizer.Add(self.getCtr().getUIByKey("SketchGridViewCtr"), flag = wx.ALIGN_CENTRE);
		fGridSizer.Add(self.pageCtrlPanel, flag = wx.EXPAND|wx.TOP, border = 8);
		fGridSizer.AddGrowableRow(1)
		self.SetSizer(fGridSizer);
		self.fGridSizer = fGridSizer;

	def updateView(self, data):
		if "gridsData" in data:
			self.updateGridsView(data["gridsData"]);
		if "title" in data:
			self.title.SetLabel(data["title"]);

	def createSketchGridViewCtr(self):
		viewHeight = self.GetSize()[1] - self.title.GetSize()[1] - self.pageCtrlPanel.GetSize()[1] - self.__params["itemRows"]; # 除减去titlePanel的高度外，还需减去边框的高度
		self.getCtr().createCtrByKey("SketchGridViewCtr", _GG("g_CommonPath") + "view/SketchGridView",
		 params = {
			"itemSize" : (self.GetSize()[0]/self.__params["itemCols"], viewHeight/self.__params["itemRows"]),
		 	"minCols" : self.__params["itemCols"]
		});

	def createTitle(self):
		self.title = wx.StaticText(self, label = self.__params["title"]);
		font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD);
		self.title.SetFont(font);

	def createPageCtrl(self):
		self.pageCtrlPanel = wx.Panel(self, size = (-1, 40));
		self.pageCtrl = PageIndexCtrl(self.pageCtrlPanel);
		self.pageCtrl.onChangeIndex = self.onChangeIndex;
		boxSizer = wx.BoxSizer(wx.VERTICAL);
		boxSizer.Add(self.pageCtrl, flag = wx.ALIGN_CENTER);
		self.pageCtrlPanel.SetSizer(boxSizer);

	def updateGridsView(self, gridsData):
		self.__randomPool.setVarList(gridsData);
		self.updateGridData();

	def updateGridData(self):
		self.getCtr().getCtrByKey("SketchGridViewCtr").updateView({
			"gridData" : self.__randomPool.getVarList(self.__params["itemCols"] * self.__params["itemRows"])
		});

	def layoutView(self, diffSize):
		if not hasattr(self,"oriSketchGridViewSize"):
			self.oriSketchGridViewSize = self.getCtr().getUIByKey("SketchGridViewCtr").GetSize();
		self.getCtr().getUIByKey("SketchGridViewCtr").updateViewSize(self.oriSketchGridViewSize + diffSize);
		self.Layout();

	def onChangeIndex(self, index):
		_GG("Log").d(index)