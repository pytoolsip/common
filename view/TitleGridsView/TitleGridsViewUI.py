# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-07 21:22:29
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-12 09:54:03

import wx;
import math;

from _Global import _GG;
from function.base import *;
from ui import ScrollView;
from data import RandomPool;

class TitleGridsViewUI(wx.Panel):
	"""docstring for TitleGridsViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(TitleGridsViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = TitleGridsViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
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
			"itemCols" : 2,
			"itemRows" : 3,
		};
		for k,v in params.items():
			self.__params[k] = v;
		# 校验itemCols和itemRows
		if self.__params["itemCols"] <= 0:
			self.__params["itemCols"] = 1;
		if self.__params["itemRows"] <= 0:
			self.__params["itemRows"] = 1;

	def getCtr(self):
		return self.viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.createTitlePanel();
		self.createSketchGridViewCtr();
		
	def initViewLayout(self):
		fGridSizer = wx.FlexGridSizer(1,1,0);
		fGridSizer.Add(self.titlePanel, flag = wx.EXPAND|wx.BOTTOM);
		fGridSizer.Add(self.getCtr().getUIByKey("SketchGridViewCtr"), flag = wx.ALIGN_CENTRE);
		fGridSizer.AddGrowableRow(1)
		self.SetSizer(fGridSizer);
		self.fGridSizer = fGridSizer;

	def updateView(self, data):
		if "gridsData" in data:
			self.updateGridsView(data["gridsData"]);
		if "title" in data:
			self.title.SetLabel(data["title"]);
		if "antBtnLabel" in data:
			self.anotherBtn.SetLabel(data["antBtnLabel"]);
		pass;

	def createSketchGridViewCtr(self):
		viewHeight = self.GetSize()[1] - self.titlePanel.GetSize()[1] - self.__params["itemRows"]; # 除减去titlePanel的高度外，还需减去边框的高度
		self.getCtr().createCtrByKey("SketchGridViewCtr", _GG("g_CommonPath") + "view\\SketchGridView",
		 params = {
			"itemSize" : (self.GetSize()[0]/self.__params["itemCols"], viewHeight/self.__params["itemRows"]),
		 	"minCols" : self.__params["itemCols"]
		});

	def createTitlePanel(self):
		self.titlePanel = wx.Panel(self, size = (-1, -1));
		self.createTitle();
		self.createAnotherBtn();
		self.initTitlePaneLayout();

	def initTitlePaneLayout(self):
		fGridSizer = wx.FlexGridSizer(0,1,0);
		fGridSizer.Add(self.title, flag = wx.EXPAND|wx.TOP, border = 4);
		fGridSizer.Add(self.anotherBtn, flag = wx.ALIGN_RIGHT);
		fGridSizer.AddGrowableCol(0)
		self.titlePanel.SetSizer(fGridSizer);

	def createTitle(self):
		self.title = wx.StaticText(self.titlePanel, label = self.__params["title"]);
		font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD);
		self.title.SetFont(font);

	def createAnotherBtn(self):
		self.anotherBtn = wx.Button(self.titlePanel, label = self.__params["antBtnLabel"], size = self.__params["antBtnSize"]);
		self.anotherBtn.Bind(wx.EVT_BUTTON, self.onAnotherBtn);

	def onAnotherBtn(self, event):
		self.updateGridData();

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