# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-04-24 22:54:42
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-16 15:09:22

try:
	import ConfigParser;
except Exception as e:
	import configparser as ConfigParser;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName",
	};

def __getExposeMethod__(DoType):
	return {
		"readIniConfig" : DoType.AddToRear,
		"writeIniConfig" : DoType.AddToRear,
		"removeIniConfig" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class IniConfigParseBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(IniConfigParseBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = IniConfigParseBehavior.__name__;

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

	# 移除ini配置文件
	def removeIniConfig(self, obj, iniFilePath, section, option = None, _retTuple = None):
		config = ConfigParser.RawConfigParser();
		config.read(iniFilePath);
		if option and config.has_option(section, option):
			config.remove_option(section, option);
			config.write(open(iniFilePath, "w"), "w");
		elif config.has_section(section):
			config.remove_section(section);
			config.write(open(iniFilePath, "w"), "w");