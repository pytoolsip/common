# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 12:45:04
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-04-05 21:59:27
import os;
import wx;
import time;

from _Global import _GG;
from function.base import *;

from MenuBarViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
	};

class MenuBarViewCtr(object):
	"""docstring for MenuBarViewCtr"""
	def __init__(self, parent, params = {}):
		super(MenuBarViewCtr, self).__init__();
		self._className_ = MenuBarViewCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件

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

	def initUI(self, parent):
		# 创建视图UI类
		self.__ui = MenuBarViewUI(parent, curPath = self._curPath, viewCtr = self);
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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "copyBehavior/ShutilCopyBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/UserServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/ToolServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.__ui.updateView(data);

	def showMessageDialog(self, message, caption = "提示", style = wx.OK):
		return wx.MessageDialog(self.getUI(), message, caption = caption, style = style).ShowModal();

	def linkToolCommon(self, toolPath = ""):
		if os.path.exists(toolPath + "/assets"):
			toolCommonPath = VerifyPath(toolPath + "/assets/common");
			if sys.platform == "win32":
				if os.system(" ".join(["mklink /J", toolCommonPath, VerifyPath(_GG("g_CommonPath"))])) != 0:
					raise Exception("<" + " ".join(["mklink /J", toolCommonPath, VerifyPath(_GG("g_CommonPath"))]) + "> fail !");
			else:
				os.system("ln -sf " + toolCommonPath + _GG("g_CommonPath"));
			return True;
		return False;

	def onClickToolDevelopment(self, menuItem, event):
		if not self.getCtrByKey("ToolDevelopInfoDialogCtr"):
			self.createCtrByKey("ToolDevelopInfoDialogCtr", _GG("g_CommonPath") + "dialog/ToolDevelopInfoDialog");
		if self.getUIByKey("ToolDevelopInfoDialogCtr").ShowModal() == wx.ID_OK :
			message = "创建工具开发项目模板失败！";
			if hasattr(self, "copyPath"):
				srcPath = _GG("g_ProjectPath") + "template";
				dstPath = self.getUIByKey("ToolDevelopInfoDialogCtr").getDirInputValue() + "/" + self.getUIByKey("ToolDevelopInfoDialogCtr").getTextCtrlValue();
				dstPath = str(dstPath);
				if self.copyPath(srcPath, dstPath):
					if self.linkToolCommon(toolPath = dstPath):
						message = "创建工具开发项目模板成功！\n创建路径为：" + VerifyPath(dstPath);
			# 显示弹窗
			self.showMessageDialog(message, "创建工具开发项目", style = wx.OK|wx.ICON_INFORMATION);

	def onClickAboutIP(self, menuItem, event):
		if not self.getCtrByKey("AboutIPDialogCtr"):
			self.createCtrByKey("AboutIPDialogCtr", _GG("g_CommonPath") + "dialog/AboutIPDialog");
		self.getUIByKey("AboutIPDialogCtr").ShowModal();

	def onOpenCurTabPagePath(self, menuItem, event):
		curTabPage = None;
		try:
			curTabPage = _GG("WindowObject").MainWindowCtr.getCtrByKey("WindowRightViewCtr").getCtrByKey("NoteBookViewCtr").getCurrentPage();
		except Exception as e:
			_GG("Log").w(e);
		# 尝试打开文件浏览器
		if curTabPage and hasattr(curTabPage, "curPath"):
			os.system("explorer " + curTabPage._curPath);
		else:
			self.showMessageDialog("打开当前标签页目录失败！", "提示", style = wx.OK|wx.ICON_INFORMATION);

	def onClickLogin(self, menuItem, event):
		self._loginIP_();

	def onClickRegister(self, menuItem, event):
		self._registerIP_();

	def onUploadTool(self, menuItem, event):
		self._uploadTool_();

	def onAddLocalTool(self, menuItem, event):
		pass;

	def getMenuItemsData(self):
		return [
			{"name" : "文件", "items" : [
				{"name" : "打开", "id" : wx.ID_OPEN, "items" : [
					{"name" : "当前标签页目录", "params" : {"helpString" : "打开当前标签页目录的文件路径..."}, "callback" : self.onOpenCurTabPagePath},
				]},
				{},
				{"name" : "退出", "id" : wx.ID_EXIT, "shortcutKey" : "Ctr+Q", "enable" : False},
			]},
			{"name" : "工具", "items" : [
				{"name" : "下载工具", "items" : [], "enable" : False},
				{"name" : "上传工具", "items" : [], "callback" : self.onUploadTool},
				{"name" : "从本地添加工具", "items" : [], "callback" : self.onAddLocalTool},
				{"name" : "进行工具开发", "items" : [], "callback" : self.onClickToolDevelopment},
			]},
			{"name" : "升级", "items" : [
				{"name" : "工具升级", "items" : [], "enable" : False},
				{"name" : "平台升级", "items" : [], "enable" : False},
			]},
			{"name" : "用户", "items" : [
				# {"name" : "用户详情", "items" : []},
				# {"name" : "需求开发", "items" : []},
				{"name" : "注销", "items" : [], "enable" : False},
				{"name" : "登录", "items" : [], "callback" : self.onClickLogin},
				{"name" : "注册", "items" : [], "callback" : self.onClickRegister},
			]},
			{"name" : "帮助", "items" : [
				{"name" : "开发工具事项", "items" : [], "enable" : False},
				{"name" : "关于", "id" : wx.ID_ABOUT, "items" : [], "callback" : self.onClickAboutIP},
			]},
		];