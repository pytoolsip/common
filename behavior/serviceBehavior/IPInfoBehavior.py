# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-03-15 16:09:17
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-15 18:40:52
import os;
try:
	import ConfigParser;
except Exception as e:
	import configparser as ConfigParser;

from _Global import _GG;
from function.base import *;

def getExposeData():
	return {
		# "exposeDataName" : {},
	};

def getExposeMethod(DoType):
	return {
		"getIPInfoConfigObj" : DoType.AddToRear,
		"getIPInfoConfig" : DoType.AddToRear,
		"setIPInfoConfig" : DoType.AddToRear,
	};

class IPInfoBehavior(_GG("BaseBehavior")):
	def __init__(self, depends = []):
		self.appendDepends(depends);
		super(IPInfoBehavior, self).__init__(depends);
		self.className_ = IPInfoBehavior.__name__;
		self.__filePath = _GG("g_DataPath") + "ptip_info.ini";

	def getExposeData(self):
		return getExposeData(); # 获取暴露出的数据

	def getExposeMethod(self, DoType):
		return getExposeMethod(DoType); # 获取暴露出的方法接口

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj.className_);
	# 	pass;

	def appendDepends(self, depends = []):
		depends.append({
			"path" : "ConfigParseBehavior/IniConfigParseBehavior",
			"basePath" : _GG("g_CommonPath") + "behavior/",
		});

	def __checkFile__(self):
		if not os.path.exists(self.__filePath):
			with open(self.__filePath, "w") as f:
				f.write("");

	def getIPInfoConfig(self, obj, _retTuple = None):
		self.__checkFile__();
		conf = ConfigParser.RawConfigParser();
		conf.read(self.__filePath);
		return conf;

	def getIPInfoConfigObj(self, obj, section, option, _retTuple = None):
		self.__checkFile__();
		return obj.readIniConfig(self.__filePath, section, option);

	def setIPInfoConfig(self, obj, section, option, value, _retTuple = None):
		self.__checkFile__();
		obj.writeIniConfig(self.__filePath, section, option, value);

	def removeIPInfoConfig(self, obj, section, option = None, _retTuple = None):
		self.__checkFile__();
		obj.removeIniConfig(self.__filePath, section, option);