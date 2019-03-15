# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-04-24 22:54:42
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-15 17:32:54

try:
	import ConfigParser;
except Exception as e:
	import configparser as ConfigParser;

from _Global import _GG;
from function.base import *;

def getExposeData():
	return {
		# "exposeDataName",
	};

def getExposeMethod(DoType):
	return {
		"readIniConfig" : DoType.AddToRear,
		"writeIniConfig" : DoType.AddToRear,
	};

class IniConfigParseBehavior(_GG("BaseBehavior")):
	def __init__(self, depends = []):
		super(IniConfigParseBehavior, self).__init__(depends);
		self.className_ = IniConfigParseBehavior.__name__;
		self.getExposeData = getExposeData; # 获取暴露出的数据
		self.getExposeMethod = getExposeMethod; # 获取暴露出的方法接口

	# 读取ini配置文件
	def readIniConfig(self, obj, iniFilePath, section, option, _retTuple = None):
		config = ConfigParser.RawConfigParser();
		config.read(iniFilePath);
		if config.has_option(section, option):
			return config.get(section, option);
		return None;

	# 读取ini配置文件
	def writeIniConfig(self, obj, iniFilePath, section, option, value, _retTuple = None):
		config = ConfigParser.RawConfigParser();
		config.read(iniFilePath);
		if not config.has_section(section):
			config.add_section(section);
		config.set(section, option, value);
		config.write(open(iniFilePath, "w"), "w");
