# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-04-22 12:01:48
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 17:27:41

import os;

from _Global import _GG;
from function.base import *;

def getExposeData():
	return {
		# "exposeDataName",
	};

def getExposeMethod(DoType):
	return {
		"verifyPythonEnvironment" : DoType.AddToRear,
		"verifyPipEnvironment" : DoType.AddToRear,
	};

class VerifyEnvironmentBehavior(_GG("BaseBehavior")):
	def __init__(self, depends = []):
		super(VerifyEnvironmentBehavior, self).__init__(depends);
		self.className_ = VerifyEnvironmentBehavior.__name__;
		self.getExposeData = getExposeData; # 获取暴露出的数据
		self.getExposeMethod = getExposeMethod; # 获取暴露出的方法接口
		pass;

	# 校验python环境
	def verifyPythonEnvironment(self, obj, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system(pythonPath.replace("\\", "/") + "/python.exe -V") == 0:
				return True;
		else:
			if os.system("python -V") == 0:
				return True;
		return False;

	def verifyPipEnvironment(self, obj, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system(pythonPath.replace("\\", "/") + "/Scripts/pip.exe -V") == 0:
				return True;
		else:
			if os.system("pip -V") == 0:
				return True;
		return False;
