# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-04-19 14:19:46
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 17:35:47

import wx;
from ProjectConfig import ProjectConfig;
from _Global import _GG;
from _Global import isExist_G;
from function.base import *;

class WindowLoader(object):
	def __init__(self):
		super(WindowLoader, self).__init__();
		self.className_ = WindowLoader.__name__;
		self.curPath = _GG("g_CommonPath") + "window/";
		self.MainApp = wx.App(self.checkIsOpenLogWin());
		self.registerEvent(); # 注册事件

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		if isExist_G(): # window加载类中的析构函数，涉及到全局变量时，要判断全局变量是否存在
			self.unregisterEvent(); # 注销事件
		pass;

	def checkIsOpenLogWin(self):
		if "isOpenLogWin" in ProjectConfig:
			return ProjectConfig["isOpenLogWin"];
		return False;

	def initWindowEvent(self):
		self.initKeyDownEvent();
		pass;

	def createWindows(self):
		self.createParentWindowCtr();
		self.createMainWindowCtr();
		# self.createSearchPanelWindowCtr();
		pass;

	def createParentWindowCtr(self):
		_GG("WindowObject").ParentWindowCtr = CreateCtr(self.curPath + "ParentWindow", None);
		self.parentWindowUI = _GG("WindowObject").ParentWindowCtr.getUI();
		
	def createMainWindowCtr(self):
		params = {
			"windowSize" : self.parentWindowUI.ClientWindow.Size,
		};
		_GG("WindowObject").MainWindowCtr = CreateCtr(self.curPath + "MainWindow", self.parentWindowUI, params = params);

	# 初始化窗口对象的公有函数
	def initWindowMethods(self):
		_GG("WindowObject").GetToolWinSize = _GG("WindowObject").MainWindowCtr.getToolWinSize; # 设置获取工具窗口大小的函数
		_GG("WindowObject").BindEventToToolWinSize = _GG("WindowObject").MainWindowCtr.bindEventToToolWinSize; # 绑定工具窗口大小变化事件
		_GG("WindowObject").UnbindEventToToolWinSize = _GG("WindowObject").MainWindowCtr.unbindEventToToolWinSize; # 解绑工具窗口大小变化事件
		_GG("WindowObject").GetMainWindowCenterPoint = _GG("WindowObject").MainWindowCtr.getMainWindowCenterPoint; # 获取主窗口的中心点
		
	def createSearchPanelWindowCtr(self):
		_GG("WindowObject").ParentWindowCtr.SearchPanelWindowCtr = CreateCtr(self.curPath + "SearchPanelWindow", self.parentWindowUI);

	def initKeyDownEvent(self):
		self.MainApp.Bind(wx.EVT_CHAR_HOOK, _GG("HotKeyManager").dispatchEvent);

	def registerEvent(self):
		_GG("EventDispatcher").register(_GG("EVENT_ID").RESTART_APP_EVENT, self, "restartApp");

	def unregisterEvent(self):
		_GG("EventDispatcher").unregister(_GG("EVENT_ID").RESTART_APP_EVENT, self, "restartApp");

	def restartApp(self, data):
		self.MainApp.ExitMainLoop(); # 退出App的主循环
		if sys.platform == "win32":
			os.system('cd ../run/&&run.vbs'); # 相对于main.py的相对路径

	def runWindows(self):
		self.parentWindowUI.Tile();
		self.parentWindowUI.Centre();
		self.parentWindowUI.Show(True);

	def runApp(self):
		self.MainApp.MainLoop();

	def createViews(self):
		wx.CallLater(100, self.onCreateViews);

	def onCreateViews(self):
		self.createHomePage();

	def createHomePage(self):
		_GG("WindowObject").MainWindowCtr.createHomePage();