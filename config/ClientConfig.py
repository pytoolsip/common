# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-02-24 05:57:41
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-09 16:40:47
import os;
import json;

try:
	import ConfigParser;
except Exception as e:
	import configparser as ConfigParser;

from _Global import _GG;
from function.base import *;

def GetConfigKeyMap():
	return {
		"Config" : _GG("g_CommonPath") + "config/ini/config.ini",
		"UrlConfig" : _GG("g_DataPath") + "url_list.json",
	};

class Config(object):
	"""docstring for Config"""
	def __init__(self, pathCfg):
		super(Config, self).__init__();
		self.__initPath__(pathCfg);
		self.__initConfig__();
	
	def __initPath__(self, pathCfg):
		if isinstance(pathCfg, list):
			for path in pathCfg:
				if os.path.exists(path):
					self.__path = path;
					return;
		self.__path = pathCfg;

	def __initConfig__(self):
		self.__config = ConfigParser.RawConfigParser();
		self.__config.read(self.__path);

	def Set(self, section, option, value):
		if not self.__config.has_section(section):
			self.__config.add_section(section);
		self.__config.set(section, option, value);
		self.__config.write(open(self.__path, "w"), "w");

	def Get(self, section, option, defaultValue = None):
		if self.__config.has_option(section, option):
			return self.__config.get(section, option);
		return defaultValue;

class UrlConfig(object):
	"""docstring for UrlConfig"""
	def __init__(self, pathCfg):
		super(UrlConfig, self).__init__();
		self.__initPath__(pathCfg);
		self.__initConfig__();
	
	def __initPath__(self, pathCfg):
		if isinstance(pathCfg, list):
			for path in pathCfg:
				if os.path.exists(path):
					self.__path = path;
					return;
		self.__path = pathCfg;

	def __initConfig__(self):
		self.__config = {};
		if os.path.exists(self.__path):
			with open(self.__path, "r") as f:
				self.__config = json.loads(f.read());

	def Get(self, t, name, key):
		for urlInfo in self.__config.get("urlList", []):
			if urlInfo.get("type", "") == t and urlInfo.get("name", "") == name:
				return urlInfo.get(key, "");
		return "";

	def GetIPVersion(self):
		return self.Get("ptip", "assets", "version");


class ClientConfig(object):
	"""docstring for ClientConfig"""
	def __init__(self,):
		super(ClientConfig, self).__init__();
		# 初始化配置对象
		confKeyMap = GetConfigKeyMap();
		self.__config = Config(confKeyMap["Config"]);
		self.__urlConfig = UrlConfig(confKeyMap["UrlConfig"]);
		pass;

	def Config(self):
		return self.__config;

	def UrlConfig(self):
		return self.__urlConfig;