# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 12:45:04
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 12:29:13

import wx;

from _Global import _GG;
from function.base import *;

class MenuBarViewUI(wx.Panel):
	"""docstring for MenuBarViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None):
		super(MenuBarViewUI, self).__init__(parent, id);
		self.className_ = MenuBarViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__parent = parent;
		self.__itemCallDict = {}; # 菜单项回调函数【key值对应菜单项ID】

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.createTopMenu();
		# self.createStatusBar();
		pass;
		
	def initViewLayout(self):
		pass;

	def createTopMenu(self):
		self.__topMenu = wx.MenuBar();
		self.__parent.SetMenuBar(self.__topMenu); # 创建菜单条
		self.__parent.Bind(wx.EVT_MENU, self.onMenu); # 绑定菜单事件
		data = {"itemsData" : self.__viewCtr.getMenuItemsData()};
		self.updateView(data);
		pass;

	def getTopMenu(self):
		return self.__topMenu;

	def createStatusBar(self):
		self.StatusBar = self.__parent.CreateStatusBar();#创建窗口底部的状态栏
		self.StatusBar.SetFieldsCount(3);
		self.StatusBar.SetStatusStyles([wx.SB_FLAT,wx.SB_FLAT,wx.SB_FLAT]);

		self.StatusBar.SetStatusWidths([-1, 350, -1]);
		self.StatusBar.SetStatusText(_GG("AppConfig")["CopryrightInfo"],1); #给状态栏设文字
		# self.StatusBar.SetStatusText("          当前用户: 梦心DH (开发)",2); #给状态栏设文字
		pass;

	# 递归创建菜单项
	def createMenuItemsByItemsData(self, parentMenu, itemsData, isMenuBar = False):
		for itemInfo in itemsData:
			if itemInfo and ("name" in itemInfo):
				# 菜单项Id
				itemId = wx.ID_ANY;
				if "id" in itemInfo:
					itemId = itemInfo["id"];
				# 菜单项标题
				showText = itemInfo["name"];
				# 如果有子菜单项，则递归创建子菜单项
				if "items" in itemInfo and len(itemInfo["items"]) > 0:
					# 创建菜单项
					theMenuItem = wx.Menu();
					# 递归创建
					self.createMenuItemsByItemsData(theMenuItem, itemInfo["items"]);
					# 将菜单项加到父项的菜单项
					if isMenuBar:
						parentMenu.Append(theMenuItem, showText);
					else:
						# parentMenu.AppendMenu(itemId, showText, theMenuItem);
						parentMenu.Append(itemId, showText, theMenuItem);
				else:
					# 设置快捷键
					if "shortcutKey" in itemInfo:
						showText += "\t" + itemInfo["shortcutKey"];
					# 菜单项其他扩展参数
					params = {};
					if "params" in itemInfo:
						params = itemInfo["params"];
					# 创建菜单项
					theMenuItem = wx.MenuItem(parentMenu, itemId, text = showText, **params);
					# 创建菜单项Icon
					if "iconImg" in itemInfo:
						theMenuItem.SetBitmap(wx.Bitmap(itemInfo["iconImg"]));
					# 绑定回调函数
					if "callback" in itemInfo and callable(itemInfo["callback"]):
						self.__itemCallDict[theMenuItem.GetId()] = itemInfo["callback"];
					# 是否允许点击
					if "enable" in itemInfo:
						theMenuItem.Enable(itemInfo["enable"]);
					# 将菜单项加到父项的单项
					parentMenu.Append(theMenuItem);
			else:
				# 如果没有菜单项信息，则添加水平条
				parentMenu.AppendSeparator();
		pass;

	def updateMenuItems(self, data):
		itemsData = data["itemsData"];
		self.createMenuItemsByItemsData(self.__topMenu, itemsData, True);
		pass;

	def updateView(self, data):
		if "itemsData" in data:
			self.updateMenuItems(data);
		pass;

	def onMenu(self, event):
		if event.GetId() in self.__itemCallDict:
			self.__itemCallDict[event.GetId()](event);
