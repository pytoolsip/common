# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-08-18 22:21:46
# @Last Modified by:   Administrator
# @Last Modified time: 2019-08-18 22:21:46
import os;
import wx;
import hashlib, json, shutil;

from _Global import _GG;

from PackDialogUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateDialog",
	};

class PackDialogCtr(object):
	"""docstring for PackDialogCtr"""
	def __init__(self, parent, params = {}):
		super(PackDialogCtr, self).__init__();
		self._className_ = PackDialogCtr.__name__;
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
		self.__ui = PackDialogUI(parent, curPath = self._curPath, viewCtr = self, params = params);
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
		_GG("BehaviorManager").bindBehavior(self, {"path" : "compileBehavior/CompilePyBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
		
	def unbindBehaviors(self):
		_GG("BehaviorManager").unbindBehavior(self, {"path" : "serviceBehavior/UpDownloadBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		_GG("BehaviorManager").unbindBehavior(self, {"path" : "compileBehavior/CompilePyBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});
		pass;
			
	def updateDialog(self, data):
		self.__ui.updateDialog(data);

	def onPackPath(self, dirPath):
		if dirPath == "":
			self.showTips("目录不能为空！");
			return;
		if not os.path.exists(dirPath):
			self.showTips("所选择的目录不存在！");
			return;
		if not os.path.isdir(dirPath):
			self.showTips("所选择的目录必须是文件夹！");
			return;
		# 开始打包文件夹
		fileName = os.path.basename(dirPath);
		if not os.path.exists(_GG("g_DataPath")+"temp/zip"):
			os.makedirs(_GG("g_DataPath")+"temp/zip");
		filePath = _GG("g_DataPath") + "temp/zip/" + "%s_%d"%(fileName, int(time.time()));
		# 压缩文件夹
		def zipFile(tgtPath):
			# 生成MD5文件列表
			self.generateMd5FileMap(tgtPath);
			# 压缩后的回调
			def finishCallback():
				shutil.rmtree(filePath); # 移除临时文件夹
				os.system("explorer " + os.path.abspath(_GG("g_DataPath") + "temp/zip"));
			self.zipFile(filePath, filePath+".zip", finishCallback = finishCallback, excludeFileType = []); # 压缩tgtPath为zip包
		# 编码文件夹
		self._compileProject_(dirPath, "/".join([filePath, fileName]), finishCallback = zipFile);

	def showTips(self, tips):
		self.__ui.showTips(tips);

	# 生成md5文件
	def generateMd5FileMap(self, dirPath):
		md5Map, md5MapPath = {}, os.path.join(dirPath, "_file_md5_map_.json");
		if os.path.exists(dirPath) and os.path.isdir(dirPath):
			for root, _, files in os.walk(dirPath):
				for fp in files:
					filePath = os.path.join(root, fp);
					with open(filePath, "rb") as f:
						md5Map[filePath.replace(dirPath, "")] = hashlib.md5(f.read()).hexdigest();
		with open(md5MapPath, "w") as f:
			f.write(json.dumps(md5Map));
		return md5MapPath;


