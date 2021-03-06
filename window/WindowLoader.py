# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-04-19 14:19:46
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-06 22:17:08

import os;
import shutil;
import wx;
from _Global import _GG;
from _Global import isExist_G;
from function.base import *;

class WindowLoader(object):
	def __init__(self):
		super(WindowLoader, self).__init__();
		self._className_ = WindowLoader.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self._mainApp = wx.App();
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
			self.unbindKeyDownEvent(); # 注销键盘点击事件
		pass;

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
		self._parentWindowUI = _GG("WindowObject").ParentWindowCtr.getUI();
		
	def createMainWindowCtr(self):
		params = {
			"windowSize" : self._parentWindowUI.ClientWindow.Size,
		};
		_GG("WindowObject").MainWindowCtr = CreateCtr(self._curPath + "MainWindow", self._parentWindowUI, params = params);

	# 初始化窗口对象的公有函数
	def initWindowMethods(self):
		self.initMainWindowMethods();
		_GG("WindowObject").CreateMessageDialog = self.createMessageDialog; # 设置显示消息弹窗函数
		_GG("WindowObject").CreateDialogCtr = self.createDialogCtr; # 设置显示弹窗控制器
		_GG("WindowObject").CreateWxDialog = self.createWxDialog; # 设置显示wx弹窗函数

	def initMainWindowMethods(self):
		_GG("WindowObject").GetToolWinSize = _GG("WindowObject").MainWindowCtr.getToolWinSize; # 设置获取工具窗口大小的函数
		_GG("WindowObject").BindEventToToolWinSize = _GG("WindowObject").MainWindowCtr.bindEventToToolWinSize; # 绑定工具窗口大小变化事件
		_GG("WindowObject").UnbindEventToToolWinSize = _GG("WindowObject").MainWindowCtr.unbindEventToToolWinSize; # 解绑工具窗口大小变化事件
		_GG("WindowObject").GetMainWindowCenterPoint = _GG("WindowObject").MainWindowCtr.getMainWindowCenterPoint; # 获取主窗口的中心点
		
	def createSearchPanelWindowCtr(self):
		_GG("WindowObject").ParentWindowCtr.SearchPanelWindowCtr = CreateCtr(self._curPath + "SearchPanelWindow", self._parentWindowUI);

	def bindKeyDownEvent(self):
		self._mainApp.Bind(wx.EVT_CHAR_HOOK, _GG("HotKeyManager").dispatchEvent);

	def unbindKeyDownEvent(self):
		self._mainApp.Unbind(wx.EVT_CHAR_HOOK);

	def registerEvent(self):
		_GG("EventDispatcher").register(_GG("EVENT_ID").STOP_APP_EVENT, self, "toStopApp");
		_GG("EventDispatcher").register(_GG("EVENT_ID").RESTART_APP_EVENT, self, "restartApp");
		_GG("EventDispatcher").register(_GG("EVENT_ID").UPDATE_APP_EVENT, self, "updateApp");

	def unregisterEvent(self):
		_GG("EventDispatcher").unregister(_GG("EVENT_ID").STOP_APP_EVENT, self, "toStopApp");
		_GG("EventDispatcher").unregister(_GG("EVENT_ID").RESTART_APP_EVENT, self, "restartApp");
		_GG("EventDispatcher").unregister(_GG("EVENT_ID").UPDATE_APP_EVENT, self, "updateApp");
	
	def toStopApp(self, data):
		if self.createMessageDialog("是否确认退出？", "退出平台", style = wx.YES_NO|wx.ICON_QUESTION, isShow = False).ShowModal() != wx.ID_YES:
			return; # 取消退出
		self.stopApp(data); # 停止App

	def stopApp(self, data):
		self._mainApp.ExitMainLoop(); # 退出App的主循环
		self.__dest__(); # 销毁回调

	def startApp(self, data):
		if sys.platform == "win32":
			# 运行执行程序
			exeName = "pytoolsip.exe";
			if os.path.exists(os.path.join(_GG("g_ProjectPath"), exeName)):
				os.system(" ".join(["start", "/d", os.path.abspath(_GG("g_ProjectPath")), exeName])); # 启动app
				return;
			# 直接运行脚本
			pyName = "pytoolsip.py";
			if os.path.exists(os.path.join(_GG("g_ProjectPath"), pyName)):
				pythonPath = "python";
				if os.path.exists(_GG("g_PythonPath")):
					pythonPath = os.path.abspath(os.path.join(_GG("g_PythonPath"), "python.exe"));
				os.system(" ".join(["start", "/d", os.path.abspath(_GG("g_ProjectPath")), pythonPath, pyName])); # 启动app
				return;
			# 运行run.bat脚本
			batName = "run.bat";
			if os.path.exists(os.path.join(_GG("g_ProjectPath"), batName)):
				os.system(" ".join(["start", "/d", os.path.abspath(_GG("g_ProjectPath")), batName])); # 启动run.bat
				return;
			# 运行失败
			_GG("Log").e("Failed to start App!");

	def restartApp(self, data):
		if self.createMessageDialog("是否确认重启？", "重启平台", style = wx.YES_NO|wx.ICON_QUESTION, isShow = False).ShowModal() != wx.ID_YES:
			return; # 取消重启
		self.stopApp(data); # 停止App
		self.startApp(data); # 开始App

	def updateApp(self, data):
		if sys.platform != "win32" or "version" not in data or "updateFile" not in data:
			self.createMessageDialog("更新平台失败！", "更新平台", style = wx.OK|wx.ICON_ERROR);
			return; # 平台更新失败
		if not self.copyUpdateVbs():
			self.createMessageDialog("更新平台失败！", "更新平台", style = wx.OK|wx.ICON_ERROR);
			return; # 平台更新失败
		# 停止App
		self.stopApp(data);
		# 调用更新脚本
		projectPath, updatePath, runPath = os.path.abspath(_GG("g_ProjectPath")), os.path.abspath(_GG("g_DataPath")+"update"), os.path.abspath(_GG("GetDependPath")("run"));
		RunCmd(" ".join([os.path.join(runPath, "update.bat"), os.path.join(_GG("g_PythonPath"), "python.exe"), os.path.abspath(data["updateFile"]), data["version"], projectPath, updatePath, updatePath]));

	def copyUpdateVbs(self):
		updateName = "update.vbs";
		runPath = os.path.abspath(_GG("GetDependPath")("run"));
		updatePath = os.path.abspath(_GG("g_DataPath")+"update");
		# 拷贝更新文件
		updateVbs = os.path.join(runPath, updateName);
		if not os.path.exists(updateVbs):
			_GG("Log").w("Failed to update IP! Not Exists updateVbs!");
			return False;
		try:
			filePath = os.path.join(updatePath, updateName);
			if os.path.exists(filePath):
				os.remove(filePath);
			shutil.copyfile(updateVbs, filePath);
			return True;
		except Exception as e:
			_GG("Log").e(f"Failed to update IP! Err[{e}]!");
		return False;

	def runWindows(self):
		self._parentWindowUI.Tile();
		self._parentWindowUI.Centre();
		self._parentWindowUI.Show(True);

	def runApp(self):
		self._mainApp.MainLoop();

	def createViews(self):
		wx.CallLater(1000, self.onCreateViews);

	def onCreateViews(self):
		self.createHomePage();

	def createHomePage(self):
		_GG("WindowObject").MainWindowCtr.createHomePage();

	def createMessageDialog(self, message, caption = "消息弹窗", style = wx.OK, isShow = True, callback = None):
		msgDialog = wx.MessageDialog(self._parentWindowUI, message, caption = caption, style = style);
		if isShow:
			result = msgDialog.ShowModal();
			if callable(callback):
				callback(msgDialog, result);
		return msgDialog;

	def createDialogCtr(self, path, params = {}, isRecreate = False, isReset = True, isShow = True, callback = None):
		# 判断是否重新创建弹窗
		if path in self.__CtrMap:
			if isRecreate:
				DelCtr(self.__CtrMap.pop(path));
		# 如果不存在弹窗，则创建弹窗
		if path not in self.__CtrMap:
			self.__CtrMap[path] = CreateCtr(path, self._parentWindowUI, params = params);
		ui = self.__CtrMap[path].getUI();
		if isReset and hasattr(ui, "resetDialog"):
			ui.resetDialog();
		if isShow:
			result = ui.ShowModal();
			if callable(callback):
				callback(ui, result);
		return ui;

	def createWxDialog(self, dialog, message, caption = "wx弹窗", style = None, isShow = False, callback = None):
		if not hasattr(wx, dialog):
			return;
		if style:
			wxDialog = getattr(wx, dialog)(self._parentWindowUI, message, caption = caption, style = style);
		else:
			wxDialog = getattr(wx, dialog)(self._parentWindowUI, message, caption = caption);
		if isShow:
			result = wxDialog.ShowModal();
			if callable(callback):
				callback(wxDialog, result);
		return wxDialog;