# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-04-22 12:01:48
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:50

import os;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName",
	};

def __getExposeMethod__(DoType):
	return {
		"verifyPythonEnvironment" : DoType.AddToRear,
		"verifyPipEnvironment" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class VerifyEnvironmentBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(VerifyEnvironmentBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__);
		self._className_ = VerifyEnvironmentBehavior.__name__;
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
