# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-04-22 12:01:48
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-16 15:09:26

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
		"verifyPythonVersion" : DoType.AddToRear,
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
		super(VerifyEnvironmentBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = VerifyEnvironmentBehavior.__name__;
		pass;

	# 校验python环境
	def verifyPythonEnvironment(self, obj, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system(os.path.abspath(os.path.join(pythonPath, "python.exe")) + " -V") == 0:
				return True;
		else:
			if os.system("python -V") == 0:
				return True;
		return False;

	# 校验python版本
	def verifyPythonVersion(self, obj, fVer = 3, sVer = 4, pythonPath = None, _retTuple = None):
		ret = "";
		if pythonPath:
			ret = os.popen(os.path.abspath(os.path.join(pythonPath, "python.exe")) + " -V").read();
		else:
			ret = os.popen("python -V").read();
		if ret:
			retList = ret.split(" ");
			if len(retList) > 1:
				vList = retList[1].split(".");
				if len(vList) < 3:
					return False;
				if int(vList[0]) >= fVer and int(vList[1]) >= sVer:
					return True;
		return False;

	def verifyPipEnvironment(self, obj, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system(os.path.abspath(os.path.join(pythonPath, "python.exe")) + " -m pip -V") == 0:
				return True;
		else:
			if os.system("pip -V") == 0:
				return True;
		return False;
