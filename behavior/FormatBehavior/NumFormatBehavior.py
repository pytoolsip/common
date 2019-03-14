# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-11 18:04:16
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 18:02:14

from _Global import _GG;
from function.base import *;
BaseBehavior = _GG("BaseBehavior");

def getExposeData():
	return {
		# "exposeDataName" : {},
	};

def getExposeMethod(DoType):
	return {
		"formtNumToChStr" : DoType.AddToRear,
	};

class NumFormatBehavior(BaseBehavior):
	def __init__(self, depends = []):
		super(NumFormatBehavior, self).__init__(depends);
		self.className_ = NumFormatBehavior.__name__;
		pass;

	def getExposeData(self):
		return getExposeData(); # 获取暴露出的数据

	def getExposeMethod(self, DoType):
		return getExposeMethod(DoType); # 获取暴露出的方法接口

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj.className_);
	# 	pass;

	def formtNumToChStr(self, obj, num, _retTuple = None):
		if isinstance(num, int):
			if num > 100000000:
				return "%.4f" % (num/100000000) + "亿"
			elif num > 10000000:
				return "%.4f" % (num/10000000) + "千万"
			elif num > 1000000:
				return "%.3f" % (num/1000000) + "百万"
			elif num > 10000:
				return "%.2f" % (num/10000) + "万"
		return num;