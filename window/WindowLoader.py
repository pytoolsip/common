# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-04-19 14:19:46
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 12:30:59

import wx;
from ProjectConfig import ProjectConfig;
from _Global import _GG;
from _Global import isExist_G;
from function.base import *;

class WindowLoader(object):
	def __init__(self):
		super(WindowLoader, self).__init__();
		self.className_ = WindowLoader.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__mainApp = wx.App(self.checkIsOpenLogWin());
		self.__CtrMap = {}; # 控制器列表
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
		self.bindKeyDownEvent();
		pass;

	def createWindows(self):
		self.createParentWindowCtr();
		self.createMainWindowCtr();
		# self.createSearchPanelWindowCtr();
		pass;

	def createParentWindowCtr(self):
		_GG("WindowObject").ParentWindowCtr = CreateCtr(self._curPath + "ParentWindow", None);
		self.__parentWindowUI = _GG("WindowObject").ParentWindowCtr.getUI();
		
	def createMainWindowCtr(self):
		params = {
			"windowSize" : self.__parentWindowUI.ClientWindow.Size,
		};
		_GG("WindowObject").MainWindowCtr = CreateCtr(self._curPath + "MainWindow", self.__parentWindowUI, params = params);

	# 初始化窗口对象的公有函数
	def initWindowMethods(self):
		_GG("WindowObject").GetToolWinSize = _GG("WindowObject").MainWindowCtr.getToolWinSize; # 设置获取工具窗口大小的函数
		_GG("WindowObject").BindEventToToolWinSize = _GG("WindowObject").MainWindowCtr.bindEventToToolWinSize; # 绑定工具窗口大小变化事件
		_GG("WindowObject").UnbindEventToToolWinSize = _GG("WindowObject").MainWindowCtr.unbindEventToToolWinSize; # 解绑工具窗口大小变化事件
		_GG("WindowObject").GetMainWindowCenterPoint = _GG("WindowObject").MainWindowCtr.getMainWindowCenterPoint; # 获取主窗口的中心点
		_GG("WindowObject").GetMainWindowCenterPoint = _GG("WindowObject").MainWindowCtr.getMainWindowCenterPoint; # 获取主窗口的中心点
		_GG("WindowObject").ShowMessageDialog = self.showMessageDialog; # 设置显示显示消息弹窗函数
		_GG("WindowObject").CreateDialogCtr = self.createDialogCtr; # 设置显示弹窗控制器
		
	def createSearchPanelWindowCtr(self):
		_GG("WindowObject").ParentWindowCtr.SearchPanelWindowCtr = CreateCtr(self._curPath + "SearchPanelWindow", self.__parentWindowUI);

	def bindKeyDownEvent(self):
		self.__mainApp.Bind(wx.EVT_CHAR_HOOK, _GG("HotKeyManager").dispatchEvent);

	def unbindKeyDownEvent(self):
		self.__mainApp.Unbind(wx.EVT_CHAR_HOOK);

	def registerEvent(self):
		_GG("EventDispatcher").register(_GG("EVENT_ID").RESTART_APP_EVENT, self, "restartApp");

	def unregisterEvent(self):
		_GG("EventDispatcher").unregister(_GG("EVENT_ID").RESTART_APP_EVENT, self, "restartApp");

	def restartApp(self, data):
		self.__mainApp.ExitMainLoop(); # 退出App的主循环
		if sys.platform == "win32":
			os.system('cd ../run/&&run.vbs'); # 相对于main.py的相对路径
		# 解绑事件
		self.unregisterEvent();
		self.unbindKeyDownEvent();

	def runWindows(self):
		self.__parentWindowUI.Tile();
		self.__parentWindowUI.Centre();
		self.__parentWindowUI.Show(True);

	def runApp(self):
		self.__mainApp.MainLoop();

	def createViews(self):
		wx.CallLater(100, self.onCreateViews);

	def onCreateViews(self):
		self.createHomePage();

	def createHomePage(self):
		_GG("WindowObject").MainWindowCtr.createHomePage();

	def showMessageDialog(self, message, caption = "消息弹窗", style = wx.OK):
		return wx.MessageDialog(self.__parentWindowUI, message, caption = caption, style = style).ShowModal();

	def createDialogCtr(self, path, params = {}, isRecreate = False, isReset = True, isShow = True, callback = None):
		# 判断是否重新创建弹窗
		if path in self.__CtrMap:
			if not isRecreate:
				return self.__CtrMap[path]
			DelCtr(self.__CtrMap[path]);
		# 创建弹窗
		self.__CtrMap[path] = CreateCtr(path, self.__parentWindowUI, params = params);
		ui = self.__CtrMap[path].getUI();
		if isReset and hasattr(ui, "resetDialog"):
			ui.resetDialog();
		if isShow:
			result = ui.ShowModal();
			if callable(callback):
				callback(ui, result);
		return ui;
