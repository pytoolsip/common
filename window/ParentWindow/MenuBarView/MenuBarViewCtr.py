# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 12:45:04
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-03 11:20:37
import os;
import wx;
import time;

from _Global import _GG;
from function.base import *;

from MenuBarViewUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateView",
		G_EVENT.LOGIN_SUCCESS_EVENT : "loginSuccessEvent",
		G_EVENT.LOGOUT_SUCCESS_EVENT : "logoutSuccessEvent",
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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/ServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateView(self, data):
		self.__ui.updateView(data);

	def showMessageDialog(self, message, caption = "提示", style = wx.OK):
		return wx.MessageDialog(self.getUI(), message, caption = caption, style = style).ShowModal();

	def initToolDevelopment(self, toolPath = ""):
		assetsPath = VerifyPath(toolPath + "/assets");
		if not os.path.exists(assetsPath):
			return False;
		# 拷贝common文件夹
		self.copyPath(VerifyPath(_GG("g_CommonPath")), VerifyPath(assetsPath + "/common"));
		# 获取main文件名称
		def getFileName(name):
			for fname in os.listdir(assetsPath):
				fPath = os.path.join(assetsPath, fname);
				if os.path.isfile(fPath) and re.search(f"{name}\.?.*\.*", fname):
					return fname;
			return f"{name}.py";
		# 更新start.bat文件
		startFilePath = VerifyPath(os.path.join(toolPath, "start.bat"));
		if os.path.exists(startFilePath):
			content = "";
			with open(startFilePath, "r", encoding = "utf-8") as f:
				for line in f.readlines():
					if re.search("set pyexe.*=.*", line):
						line = "set pyexe=" + VerifyPath(_GG("g_PythonPath")+"/python.exe") + "\n";
					elif re.search("set mainfile.*=.*", line):
						line = "set mainfile=" + VerifyPath(getFileName("main")) + "\n";
					elif re.search("set buildfile.*=.*", line):
						line = "set buildfile=" + VerifyPath(getFileName("build")) + "\n";
					content += line;
			with open(startFilePath, "w", encoding = "utf-8") as f:
				f.write(content);
		return True;

	def onClickToolDevelopment(self, menuItem, event):
		if not self.getCtrByKey("ToolDevelopInfoDialogCtr"):
			self.createCtrByKey("ToolDevelopInfoDialogCtr", _GG("g_CommonPath") + "dialog/ToolDevelopInfoDialog");
		if self.getUIByKey("ToolDevelopInfoDialogCtr").ShowModal() == wx.ID_OK :
			message = "创建工具开发项目模板失败！";
			if hasattr(self, "copyPath"):
				srcPath = os.path.join(_GG("GetDependPath")("template"), "tool");
				dstPath = self.getUIByKey("ToolDevelopInfoDialogCtr").getDirInputValue() + "/" + self.getUIByKey("ToolDevelopInfoDialogCtr").getTextCtrlValue();
				dstPath = str(dstPath);
				if self.copyPath(srcPath, dstPath) and self.initToolDevelopment(toolPath = dstPath):
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
		if curTabPage and hasattr(curTabPage, "_curPath"):
			os.system("explorer " + os.path.abspath(curTabPage._curPath));
		else:
			self.showMessageDialog("打开当前标签页目录失败！", "提示", style = wx.OK|wx.ICON_INFORMATION);

	def onClickLogin(self, menuItem, event):
		self._loginIP_();

	def onDownloadTool(self, menuItem, event):
		self._downloadTool_();

	def onAddLocalTool(self, menuItem, event):
		def onOk(localToolInfo):
			# 更新左侧工具树
			_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_WINDOW_LEFT_VIEW, {
				"action" : "add",
				"key" : localToolInfo["tkey"],
				"trunk" : "g_DataPath",
				"branch" : "/".join(["tools", "local", localToolInfo["tkey"], "tool"]),
				"path" : "MainView",
				"name" : localToolInfo["name"],
				"category" : localToolInfo["category"],
				"description" : localToolInfo["description"],
				"version" : "无",
				"author" : "本地",
			});
			return True;
		def checkToolKey(tkey):
			return not _GG("WindowObject").MainWindowCtr.getCtrByKey("WindowLeftViewCtr").checkItemKey(tkey);
		_GG("WindowObject").CreateDialogCtr(_GG("g_CommonPath") + "dialog/AddLocalToolDialog", params = {
			"onOk" : onOk,
			"checkToolKey" : checkToolKey,
		});

	def onSearchTool(self, menuItem, event):
		if self.showMessageDialog("搜索工具需要打开浏览器，是否确认打开？", "打开浏览器提示", style = wx.OK|wx.CANCEL|wx.ICON_QUESTION) == wx.ID_OK:
			wx.LaunchDefaultBrowser(_GG("AppConfig")["SearchToolUrl"]);
		# _GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_WINDOW_RIGHT_VIEW, {
		# 	"createPage" : True,
		# 	"key" : "e3a0dfe5561d51fdfb75c3b7d2909b47",
		# 	"pagePath" : _GG("g_CommonPath") + "view/SearchToolView",
		# 	"category" : "菜单/",
		# 	"title" : "工具-搜索工具"
		# });

	def onClickLogout(self, menuItem, event):
		self._logoutIP_();

	def loginSuccessEvent(self, data):
		topMenu = self.getUI().getTopMenu();
		itemIdList = [topMenu.FindMenuItem("用户", "登录")];
		for itemId in itemIdList:
			topMenu.Enable(itemId, False);
		itemId = topMenu.FindMenuItem("用户", "登出");
		topMenu.Enable(itemId, True);
		pass;

	def logoutSuccessEvent(self, data):
		topMenu = self.getUI().getTopMenu();
		itemId = topMenu.FindMenuItem("用户", "登出");
		topMenu.Enable(itemId, False);
		itemIdList = [topMenu.FindMenuItem("用户", "登录")];
		for itemId in itemIdList:
			topMenu.Enable(itemId, True);
		pass;

	def onPackTool(self, menuItem, event):
		if not self.getCtrByKey("PackDialogCtr"):
			self.createCtrByKey("PackDialogCtr", _GG("g_CommonPath") + "dialog/PackDialog");
		self.getUIByKey("PackDialogCtr").ShowModal();

	def onOpenProjectPath(self, menuItem, event):
		try:
			os.system("explorer " + os.path.abspath(_GG("g_ProjectPath")));
		except Exception as e:
			_GG("Log").w(e);
			self.showMessageDialog("打开安装目录失败！", "提示", style = wx.OK|wx.ICON_INFORMATION);

	def onOpenSettingDialog(self, menuItem, event):
		if not self.getCtrByKey("SettingDialogCtr"):
			self.createCtrByKey("SettingDialogCtr", _GG("g_CommonPath") + "dialog/SettingDialog");
		self.getCtrByKey("SettingDialogCtr").resetDialog();
		self.getUIByKey("SettingDialogCtr").ShowModal();
	
	def onCreateTemplate(self, menuItem, event):
		def onOk(targetPath):
			try:
				os.system("explorer " + os.path.abspath(targetPath));
			except Exception as e:
				_GG("Log").w(e);
				self.showMessageDialog("打开所创建模板的目录失败！", "提示", style = wx.OK|wx.ICON_INFORMATION);
		if not self.getCtrByKey("CreateTemplateDialogCtr"):
			self.createCtrByKey("CreateTemplateDialogCtr", _GG("g_CommonPath") + "dialog/CreateTemplateDialog", params={
				"onOk" : onOk,
			});
		self.getCtrByKey("CreateTemplateDialogCtr").resetDialog();
		self.getUIByKey("CreateTemplateDialogCtr").ShowModal();
		pass;

	def onCheckUpdateIP(self, menuItem, event):
		def callback(resp):
			if resp and resp.code == 0:
				if self.showMessageDialog("检测有更新版本，是否确认更新？", "平台更新", style = wx.YES_NO|wx.ICON_QUESTION) == wx.ID_YES:
					self.updateIP(resp.version);
			else:
				self.showMessageDialog("平台版本已是最新！", "提示", style = wx.OK|wx.ICON_INFORMATION);
		self.requestUpdateIP(callback = callback);
		pass;

	def getMenuItemsData(self):
		return [
			{"name" : "文件", "items" : [
				{"name" : "打开", "id" : wx.ID_OPEN, "items" : [
					{"name" : "平台安装目录", "params" : {"helpString" : "打开平台安装路径..."}, "callback" : self.onOpenProjectPath},
					{"name" : "当前标签页目录", "params" : {"helpString" : "打开当前标签页目录的文件路径..."}, "callback" : self.onOpenCurTabPagePath},
				]},
				{"name" : "设置", "params" : {"helpString" : "打开平台设置..."}, "callback" : self.onOpenSettingDialog},
				{},
				{"name" : "退出", "id" : wx.ID_EXIT, "enable" : False},
			]},
			{"name" : "编辑", "items" : [
				{"name" : "新建模板", "items" : [], "callback" : self.onCreateTemplate},
			]},
			{"name" : "工具", "items" : [
				{"name" : "搜索工具", "items" : [], "callback" : self.onSearchTool},
				{"name" : "下载工具", "items" : [], "callback" : self.onDownloadTool},
				{},
				{"name" : "打包工具", "items" : [], "callback" : self.onPackTool},
				{},
				{"name" : "从本地添加工具", "items" : [], "callback" : self.onAddLocalTool},
				{"name" : "开发工具", "items" : [], "callback" : self.onClickToolDevelopment},
			]},
			{"name" : "升级", "items" : [
				{"name" : "工具升级", "items" : [], "enable" : False},
				{"name" : "平台升级", "items" : [], "callback" : self.onCheckUpdateIP},
			]},
			{"name" : "用户", "items" : [
				# {"name" : "用户详情", "items" : []},
				# {"name" : "需求开发", "items" : []},
				{"name" : "登出", "items" : [], "callback" : self.onClickLogout, "enable" : False},
				{"name" : "登录", "items" : [], "callback" : self.onClickLogin},
			]},
			{"name" : "帮助", "items" : [
				{"name" : "开发工具事项", "items" : [], "enable" : False},
				{"name" : "关于", "id" : wx.ID_ABOUT, "items" : [], "callback" : self.onClickAboutIP},
			]},
		];