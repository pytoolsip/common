# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-19 14:22:56
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2020-02-02 21:19:55
import wx;
import os,sys,time;
import shutil;
# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
# 添加搜索路径
if CURRENT_PATH not in sys.path:
	sys.path.append(CURRENT_PATH);
if os.path.join(CURRENT_PATH, "core") not in sys.path:
	sys.path.append(os.path.join(CURRENT_PATH, "core"));

# 加载工程
import _Global as _G;
from window.WindowLoader import WindowLoader;
from behaviorCore.BaseBehavior import BaseBehavior;
from behaviorCore.BehaviorManager import BehaviorManager;
from eventDispatchCore.EventDispatcher import EventDispatcher;
from eventDispatchCore.EventId import EVENT_ID;
from hotKeyCore.HotKeyManager import HotKeyManager;
from timerCore.TimerManager import TimerManager;
from logCore.Logger import Logger;
from cacheCore.CacheManager import CacheManager;

from net import CommonClient;
from config import AppConfig;
from config import ClientConfig;


class GlobalWindowObject(object):
	def __init__(self):
		super(GlobalWindowObject, self).__init__();
		pass;

class Loader(object):
	def __init__(self, mainPath, projectPath):
		super(Loader, self).__init__();
		self._className_ = Loader.__name__;
		self.__mainPath = mainPath.replace("\\", "/");
		self.__projectPath = projectPath.replace("\\", "/");
		_G.initGlobal_GTo_Global(); # 初始化全局变量
		pass;

	def getWindowLoader(self):
		if not hasattr(self,"WindowLoader"):
			self.WindowLoader = WindowLoader();
		return self.WindowLoader;

	def lockGlobal(self):
		_G.lockGlobal_GTo_Global(); # 锁定全局变量

	def loadGlobalInfo(self):
		self.loadUniqueIdFunc(); # 加载唯一Id的全局函数
		self.loadPaths(); # 加载全局路径名变量
		self.loadDependPath(); # 加载全局依赖路径名变量
		self.loadPyPath(); # 加载全局python路径变量
		self.loadObjects(); # 加载全局对象变量
		self.loadConfigs(); # 加载全局配置变量
		self.loadResources(); # 加载全局资源变量
		self.loadGClass(); # 加载全局类变量
		pass;

	# 加载唯一Id的全局函数
	def loadUniqueIdFunc(self):
		global uniqueId;
		uniqueId = 0;
		def getUniqueId():
			global uniqueId;
			uniqueId += 1;
			return uniqueId;
		_G.setGlobalVarTo_Global("getUniqueId", getUniqueId);

	# 加载全局路径名变量
	def loadPaths(self):
		_G.setGlobalVarTo_Global("g_ProjectPath", self.__projectPath + "/");
		_G.setGlobalVarTo_Global("g_DataPath", self.__projectPath + "/data/");
		if not os.path.exists(_G._GG("g_DataPath")):
			os.makedirs(_G._GG("g_DataPath")); # 若工程数据文件不存在，则需创建该目录
		_G.setGlobalVarTo_Global("g_AssetsPath", self.__mainPath + "/");
		_G.setGlobalVarTo_Global("g_CommonPath", self.__mainPath + "/common/");
		pass;

	def loadDependPath(self):
		def getDependPath(path):
			dependPath = os.path.abspath(os.path.join(self.__mainPath, "..", path));
			if os.path.exists(dependPath):
				return dependPath;
			return os.path.abspath(os.path.join(self.__projectPath, path));
		_G.setGlobalVarTo_Global("GetDependPath", getDependPath);

	# 加载全局python路径变量
	def loadPyPath(self):
		_G.setGlobalVarTo_Global("g_PythonPath", _G._GG("GetDependPath")("include/python"));

	# 更新全局python路径变量
	def updatePyPath(self, path):
		_G.setGlobalVarTo_Global("g_PythonPath", path, isCover=True);

	# 加载全局对象变量
	def loadObjects(self):
		_G.setGlobalVarTo_Global("BaseBehavior", BaseBehavior); # 设置组件基础类变量（未实例化）
		_G.setGlobalVarTo_Global("WindowObject", GlobalWindowObject()); # 设置窗口类的全局变量
		_G.setGlobalVarTo_Global("BehaviorManager", BehaviorManager()); # 设置组件管理器的全局变量
		_G.setGlobalVarTo_Global("EventDispatcher", EventDispatcher()); # 设置事件分发器的全局变量
		_G.setGlobalVarTo_Global("EVENT_ID", EVENT_ID); # 设置事件枚举Id的全局变量
		_G.setGlobalVarTo_Global("HotKeyManager", HotKeyManager()); # 设置热键管理器的全局变量
		_G.setGlobalVarTo_Global("TimerManager", TimerManager()); # 设置定时器管理器的全局变量
		_G.setGlobalVarTo_Global("CacheManager", CacheManager()); # 设置缓存管理器的全局变量
		pass;

	# 加载全局配置变量
	def loadConfigs(self):
		print("Loading configs......");
		_G.setGlobalVarTo_Global("AppConfig", AppConfig);
		_G.setGlobalVarTo_Global("ClientConfig", ClientConfig()); # 设置客户端配置的全局变量
		print("Loaded configs!");
		pass;

	# 加载全局资源变量
	def loadResources(self):
		print("Loading resources......");
		print("Loaded resources!");
		pass;

	def loadGClass(self):
		self.loadLogger(); # 加载日志类变量
		self.loadCommonClient(); # 加载客户端->服务端连接变量
		pass;

	def loadLogger(self):
		cliConf = _G._GG("ClientConfig").Config(); # 服务配置
		path = cliConf.Get("log", "path", "").replace("\\", "/");
		name = cliConf.Get("log", "name", "pytoolsip-client");
		curTimeStr = time.strftime("%Y_%m_%d", time.localtime());
		logger = Logger("Common", isLogFile = True, logFileName = os.path.join(self.__projectPath, path, name+("_%s.log"%curTimeStr)),
			maxBytes = int(cliConf.Get("log", "maxBytes")), backupCount = int(cliConf.Get("log", "backupCount")));
		_G.setGlobalVarTo_Global("Log", logger); # 设置日志类的全局变量
		return logger;

	# 加载客户端->服务端连接变量
	def loadCommonClient(self):
		_G.setGlobalVarTo_Global("CommonClient", CommonClient()); # 设置客户端->服务端连接的全局变量
		pass;

	# 初始化全局对象
	def initGlobalClass(self):
		_G._GG("CommonClient").initClient();

	# 校验默认数据
	def verifyDefaultData(self):
		_GG = _G._GG;
		# 校验配置文件夹
		if not os.path.exists(_GG("g_DataPath")+"config"):
			os.makedirs(_GG("g_DataPath")+"config");
		# 校验工具树配置
		if not os.path.exists(_GG("g_DataPath")+"config/tools_tree.json"):
			shutil.copyfile(_GG("g_CommonPath") + "config/json/toolsTree.json", _GG("g_DataPath")+"config/tools_tree.json");
		# 校验临时文件夹
		if not os.path.exists(_GG("g_DataPath")+"temp"):
			os.makedirs(_GG("g_DataPath")+"temp");
		# 校验工具文件夹
		if not os.path.exists(_GG("g_DataPath")+"tools"):
			os.makedirs(_GG("g_DataPath")+"tools");
		# 校验更新文件夹
		if not os.path.exists(_GG("g_DataPath")+"update"):
			os.makedirs(_GG("g_DataPath")+"update");
		# 校验缓存文件夹
		if not os.path.exists(_GG("g_DataPath")+"cache"):
			os.makedirs(_GG("g_DataPath")+"cache");