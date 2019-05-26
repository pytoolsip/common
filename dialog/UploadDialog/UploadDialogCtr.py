# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-16 03:04:58
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-24 12:27:37
import os;
import wx;
import zipfile, json;

from _Global import _GG;

from UploadDialogUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateDialog",
	};

class UploadDialogCtr(object):
	"""docstring for UploadDialogCtr"""
	def __init__(self, parent, params = {}):
		super(UploadDialogCtr, self).__init__();
		self._className_ = UploadDialogCtr.__name__;
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
		self.__ui = UploadDialogUI(parent, curPath = self._curPath, viewCtr = self, params = params);
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
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateDialog(self, data):
		self.__ui.updateDialog(data);

	def onInputToolFile(self, filePath, callback):
		if filePath != "" and os.path.exists(filePath):
			if os.path.isdir(filePath):
				if os.path.exists(filePath+"/tool.json"):
					fileName = os.path.basename(filePath);
					if not os.path.exists(_GG("g_DataPath")+"temp/zip"):
						os.mkdir(_GG("g_DataPath")+"temp/zip");
					zipFilePath = _GG("g_DataPath") + "temp/zip/" + "%s_%d.zip"%(fileName, int(time.time()));
					def finishCallback():
						self.updateDialogByZipFile(zipFilePath);
					if self.zipFile(filePath, zipFilePath, finishCallback = finishCallback): # 压缩filePath为zip包
						filePath = zipFilePath; # 重置filePath
				else:
					_GG("WindowObject").CreateMessageDialog("上传工程路径有误【缺失tool.json文件】，请重新选择！", "上传工具", style = wx.OK|wx.ICON_ERROR);
					return callback("");
			else:
				self.updateDialogByZipFile(filePath);
		return callback(zipFilePath);

	def updateDialogByZipFile(self, filePath):
		if os.path.splitext(filePath)[-1] == ".zip":
			zfile = zipfile.ZipFile(filePath);
			try:
				toolJsonStr = bytes.decode(zfile.read('tool.json'));
				self.getUI().updateDialog(json.loads(toolJsonStr));
			except Exception as e:
				_GG("WindowObject").CreateMessageDialog("上传工具包的json文件数据有误！\n%s"%e, "上传工具", style = wx.OK|wx.ICON_ERROR);

	def checkNameFormat(self, name):
		if re.match(r"^[_a-zA-Z0-9\u4e00-\u9fa5]+$", name):
			return True;
		return False;

	def checkVersion(self, version, onlineVersion, IPVersion):
		newVerVal = None;
		verList = [int(ver) for ver in version.replace(" ", "").split(".") if ver.isdigit()];
		comVerList = [int(ver) for ver in IPVersion.split(".")];
		if len(verList) != 3 or (verList[0] <= 0 and verList[1] <= 0 and verList[2] <= 0):
			return False, "版本格式错误！", newVerVal;
		if verList[0] != comVerList[0]:
			return False, "版本第1位必须与common版本的相同！", newVerVal;
		if onlineVersion == "无":
			if verList[0] == comVerList[0] and verList[1] == 0 and verList[2] == 0:
				return True, "", ".".join([str(ver) for ver in verList]);
			return False, "初始版本必须为%d.0.0！"%comVerList[0], ".".join([str(ver) for ver in verList]);
		olVerList = [int(ver) for ver in onlineVersion.split(".")];
		if olVerList[1] > verList[1]:
			return False, "版本第2位不能小于线上版本的！", ".".join([str(ver) for ver in verList]);
		elif olVerList[1] < verList[1]:
			if verList[1] - olVerList[1]:
				return False, "版本第2位增量必须为1！", ".".join([str(ver) for ver in verList]);
			if verList[2] != 0:
				return False, "更新版本第2位时，第3位必须为0！", ".".join([str(ver) for ver in verList]);
		else:
			if olVerList[2] > verList[2]:
				return False, "版本第3位不能小于线上版本的！", ".".join([str(ver) for ver in verList]);
			if verList[2] - olVerList[2] != 1:
				return False, "版本第3位增量必须为1！", ".".join([str(ver) for ver in verList]);
		return True, "", ".".join([str(ver) for ver in verList]);

	def checkExCategory(self, exCategory):
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