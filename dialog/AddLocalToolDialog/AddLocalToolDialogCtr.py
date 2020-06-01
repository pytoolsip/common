# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-04-05 22:36:48
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-13 20:18:57
import os;
import wx;
import shutil;
import hashlib,threading;

from _Global import _GG;

from AddLocalToolDialogUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateDialog",
	};

class AddLocalToolDialogCtr(object):
	"""docstring for AddLocalToolDialogCtr"""
	def __init__(self, parent, params = {}):
		super(AddLocalToolDialogCtr, self).__init__();
		self._className_ = AddLocalToolDialogCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
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

	def initUI(self, parent, params):
		# 创建视图UI类
		self.__ui = AddLocalToolDialogUI(parent, curPath = self._curPath, viewCtr = self, params = params);
		self.__ui.initDialog();

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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/UpDownloadBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		_GG("BehaviorManager").bindBehavior(self, {"path" : "CopyBehavior/ShutilCopyBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/ToolServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateDialog(self, data):
		self.__ui.updateDialog(data);

	def checkNameFormat(self, name):
		if re.match(r"^[_a-zA-Z0-9\u4e00-\u9fa5]+$", name):
			return True;
		return False;

	def checkCategory(self, exCategory):
		if not re.match(r"^[/_a-zA-Z0-9\u4e00-\u9fa5]+$", exCategory):
			return False, "不能包含特殊字符！";
		exList = exCategory.split("/");
		if len(exList) > 2:
			return False, "不能扩展分类超过2级！";
		return True, "";

	def verifyCategory(self, category):
		category = category.replace(" ", "");
		if len(category) > 0 and category[-1] != "/":
			category += "/";
		return category;

	def verifyBackslash(self, value):
		value = value.replace(" ", "");
		if len(value) > 0 and value[-1] == "/":
			value = value[:-1];
		return value;

	def getKeyByName(self, name):
		return hashlib.md5(name.encode("utf-8")).hexdigest();

	def addLocalTool(self, toolInfo, callback = None):
		def toAddTool(localToolInfo, callback):
			localToolPath = _GG("g_DataPath")+"tools/local/";
			filePath = localToolInfo["filePath"];
			fullName = localToolInfo["category"] + "/" + localToolInfo["name"];
			tkey = localToolInfo["tkey"];
			targetPath = localToolPath + tkey;
			if os.path.exists(targetPath):
				if wx.MessageDialog(self.getUI(), f"已存在同名工具[{fullName}]文件，是否覆盖该工具文件？", caption = "添加本地工具", style = wx.YES_NO|wx.ICON_QUESTION).ShowModal() != wx.ID_YES:
					return;
				shutil.rmtree(targetPath);
			if os.path.splitext(filePath)[-1] == ".zip":
				self.unzipFile(filePath, targetPath);
			else:
				self.copyPath(filePath, targetPath+"/tool");
			def afterDealDepends():
				if callable(callback):
					wx.CallAfter(callback, localToolInfo);
			def failDealDepends():
				shutil.rmtree(targetPath);
			wx.CallAfter(self._dealDepends_, tkey, "", targetPath + "/tool", finishCallback = afterDealDepends, failedCallback = failDealDepends);
		threading.Thread(target = toAddTool, args = (toolInfo, callback)).start();