# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 14:46:20
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 14:33:56

import wx;

from _Global import _GG;
from function.base import *;

class WindowLeftViewUI(wx.Panel):
	"""docstring for WindowLeftViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None):
		super(WindowLeftViewUI, self).__init__(parent, id);
		self._className_ = WindowLeftViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.createTitleText();
		self.createUserNameTextCtr();
		self.createTreeCtrl();
		self.line = wx.StaticLine(self)
		pass;
		
	def initViewLayout(self):
		# 创建flexGridSizer，并设置相应控件和参数
		self.flexGridSizer = wx.FlexGridSizer(4, 0, 2, 2);
		self.flexGridSizer.AddMany([
			(self.getCtr().getUIByKey("UserNameTextViewCtr"), -1, wx.EXPAND),
			(self.line, -1, wx.EXPAND),
			(self.listTitleText, -1, wx.EXPAND),
			(self.getCtr().getUIByKey("TreeItemsViewCtr"), -1, wx.EXPAND)
		]);
		self.flexGridSizer.AddGrowableCol(0, 1);
		self.flexGridSizer.AddGrowableRow(3, 0);
		# 将整个flexGridSizer扩充到整个左边的窗口
		leftBox = wx.BoxSizer(wx.HORIZONTAL);
		leftBox.Add(self.flexGridSizer, proportion = 2, flag = wx.ALL|wx.EXPAND, border = 4);
		self.SetSizer(leftBox);
		pass;

	def updateView(self, data):
		pass;

	def createTitleText(self):
		# 创建文本
		self.listTitleText = wx.StaticText(self, -1, u"工具列表:", style = wx.ALIGN_LEFT);
		# 设置文本颜色
		self.listTitleText.SetForegroundColour(wx.Colour(108,108,108));
		# 设置文本字体
		titleFont = wx.Font(8, wx.DECORATIVE, wx.NORMAL, wx.BOLD);
		self.listTitleText.SetFont(titleFont);
		pass;

	def createUserNameTextCtr(self):
		self.getCtr().createCtrByKey("UserNameTextViewCtr", _GG("g_CommonPath") + "view/UserNameTextView", params = {
			"onClick" : self.getCtr().onClickLogin,
		}); # , parent = self, params = {}
		
	def createTreeCtrl(self):
		params = {
			"defaultItemsData" : self.getCtr().getTreeItemsDataByFilePath(_GG("g_DataPath")+"tools_tree.xml"),
		};
		self.getCtr().createCtrByKey("TreeItemsViewCtr",
			_GG("g_CommonPath") + "view/TreeItemsView",
			parent = self, params = params);
		pass;