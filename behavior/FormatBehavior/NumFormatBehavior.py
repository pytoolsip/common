# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-11 18:04:16
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-16 15:09:23

from _Global import _GG;
from function.base import *;
BaseBehavior = _GG("BaseBehavior");

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"formtNumToChStr" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class NumFormatBehavior(BaseBehavior):
	def __init__(self):
		super(NumFormatBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = NumFormatBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
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