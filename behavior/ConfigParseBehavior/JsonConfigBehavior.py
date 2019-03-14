# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-24 02:42:20
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 18:02:11

from _Global import _GG;
from function.base import *;
BaseBehavior = _GG("BaseBehavior");

def getExposeData():
	return {
		# "exposeDataName" : {},
	};

def getExposeMethod(DoType):
	return {
		"writeJsonFile" : DoType.AddToRear,
		"readJsonFile" : DoType.AddToRear,
	};

class JsonConfigBehavior(BaseBehavior):
	def __init__(self, depends = []):
		super(JsonConfigBehavior, self).__init__(depends);
		self.className_ = JsonConfigBehavior.__name__;
		pass;

	def getExposeData(self):
		return getExposeData(); # 获取暴露出的数据

	def getExposeMethod(self, DoType):
		return getExposeMethod(DoType); # 获取暴露出的方法接口

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj.className_);
	# 	pass;

	def writeJsonFile(self, obj, filePath, data, _retTuple = None):
		with open(filePath, "w") as f:
			f.write(json.dumps(data, indent=4));
			f.close();

	def readJsonFile(self, obj, filePath, _retTuple = None):
		data = None;
		with open(filePath, "rb") as f:
			data = json.loads(f.read().decode("utf-8", "ignore"));
			f.close();
		return data;
