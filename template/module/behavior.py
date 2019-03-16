# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-29 22:19:40
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 11:24:28

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		# "defaultFun" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class TemplateBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(TemplateBehavior, self).__init__(__getDepends__());
		self.className_ = TemplateBehavior.__name__;
		pass;

	def getExposeData(self):
		return __getExposeData__(); # 获取暴露出的数据

	def getExposeMethod(self, DoType):
		return __getExposeMethod__(DoType); # 获取暴露出的方法接口

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj.className_);
	# 	pass;

