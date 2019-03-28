# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-24 02:42:20
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-28 18:54:57
import json;

from _Global import _GG;
from function.base import *;
BaseBehavior = _GG("BaseBehavior");

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"writeJsonFile" : DoType.AddToRear,
		"readJsonFile" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class JsonConfigBehavior(BaseBehavior):
	def __init__(self):
		super(JsonConfigBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = JsonConfigBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	def writeJsonFile(self, obj, filePath, data, _retTuple = None):
		with open(filePath, "w") as f:
			f.write(json.dumps(data, indent=4));
			f.close();

	def readJsonFile(self, obj, filePath, _retTuple = None):
		data = None;
		with open(filePath, "rb") as f:
			data = json.loads(f.read().decode("utf-8"));
			f.close();
		return data;
