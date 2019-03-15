# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-03-15 16:09:17
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-15 17:34:57
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
		"getIPInfoConfig" : DoType.AddToRear,
		"readIPInfoConfig" : DoType.AddToRear,
		"writeIPInfoConfig" : DoType.AddToRear,
	};

class IPInfoBehavior(_GG("BaseBehavior")):
	def __init__(self, depends = []):
		self.appendDepends(depends);
		super(IPInfoBehavior, self).__init__(depends);
		self.className_ = IPInfoBehavior.__name__;
		self.__dirPath = _GG("g_ProjectPath")+"date/";
		self.__fileName = "ptip_info.ini";

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

	def checkIPInfoFile(self):
		if not os.path.exists(self.__dirPath):
			os.mkdir(self.__dirPath);
		if not os.path.exists(self.__dirPath + self.__fileName):
			with open(self.__dirPath + self.__fileName, "w") as f:
				f.write("");

	def getIPInfoConfig(self, obj, _retTuple = None):
		self.checkIPInfoFile();
		conf = ConfigParser.RawConfigParser();
		conf.read(self.__dirPath + self.__fileName);
		return conf;

	def readIPInfoConfig(self, obj, section, option, _retTuple = None):
		self.checkIPInfoFile();
		return obj.readIniConfig(self.__dirPath + self.__fileName, section, option);

	def writeIPInfoConfig(self, obj, section, option, value, _retTuple = None):
		self.checkIPInfoFile();
		obj.writeIniConfig(self.__dirPath + self.__fileName, section, option, value);