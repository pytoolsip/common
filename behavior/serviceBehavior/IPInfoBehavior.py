# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-03-15 16:09:17
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-05 15:26:27
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import os;
try:
	import ConfigParser;
except Exception as e:
	import configparser as ConfigParser;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"getIPInfoConfigObj" : DoType.AddToRear,
		"getIPInfoConfig" : DoType.AddToRear,
		"setIPInfoConfig" : DoType.AddToRear,
		"removeIPInfoConfig" : DoType.AddToRear,
		"setEncodePublicKey" : DoType.AddToRear,
		"encodeStrByPublicKey" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		{
			"path" : "ConfigParseBehavior/IniConfigParseBehavior",
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
	];

class IPInfoBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(IPInfoBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = IPInfoBehavior.__name__;
		self.__filePath = _GG("g_DataPath") + "config/ptip_info.ini";

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	def __checkFile__(self):
		if not os.path.exists(self.__filePath):
			with open(self.__filePath, "w") as f:
				f.write("");

	def getIPInfoConfigObj(self, obj, _retTuple = None):
		self.__checkFile__();
		conf = ConfigParser.RawConfigParser();
		conf.read(self.__filePath);
		return conf;

	def getIPInfoConfig(self, obj, section, option, _retTuple = None):
		self.__checkFile__();
		return obj.readIniConfig(self.__filePath, section, option);

	def setIPInfoConfig(self, obj, section, option, value, _retTuple = None):
		self.__checkFile__();
		obj.writeIniConfig(self.__filePath, section, option, value);

	def removeIPInfoConfig(self, obj, section, option = None, _retTuple = None):
		self.__checkFile__();
		obj.removeIniConfig(self.__filePath, section, option);

	def setEncodePublicKey(self, obj, value, _retTuple = None):
		obj.setIPInfoConfig("encode", "public_key", value);

	def encodeStrByPublicKey(self, obj, value, _retTuple = None):
		publicKey = obj.getIPInfoConfig("encode", "public_key");
		if publicKey:
			rsakey = RSA.importKey(publicKey);
			cipher = Cipher_pkcs1_v1_5.new(rsakey);
			return base64.b64encode(cipher.encrypt(str.encode(value)));
		return "";