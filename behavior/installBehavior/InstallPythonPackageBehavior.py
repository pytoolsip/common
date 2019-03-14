# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-04-23 22:18:59
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 18:02:15

import os;
import imp;

from _Global import _GG;
from function.base import *;

def getExposeData():
	return {
		# "exposeDataName",
	};

def getExposeMethod(DoType):
	return {
		"getInstalledPackagesByPip" : DoType.AddToRear,
		"installPackageByPip" : DoType.AddToRear,
		"updatePipVersion" : DoType.AddToRear,
		"checkPackageIsInstalled" : DoType.AddToRear,
		"installPipByEasyInstall" : DoType.AddToRear,
	};

class InstallPythonPackageBehavior(_GG("BaseBehavior")):
	def __init__(self, depends = []):
		super(InstallPythonPackageBehavior, self).__init__(depends);
		self.className_ = InstallPythonPackageBehavior.__name__;
		self.getExposeData = getExposeData; # 获取暴露出的数据
		self.getExposeMethod = getExposeMethod; # 获取暴露出的方法接口

	# 获取已通过pip安装的包
	def getInstalledPackagesByPip(self, obj, pythonPath = None, _retTuple = None):
		installedPackageDict = {};
		if pythonPath:
			installedPackageReader = os.popen(pythonPath.replace("\\", "/") + "/Scripts/pip.exe freeze");
		else:
			installedPackageReader = os.popen("pip freeze");
		installedPackageLines = installedPackageReader.read();
		for line in installedPackageLines.splitlines():
			lineArr = line.split("==");
			if len(lineArr) == 2:
				installedPackageDict[lineArr[0]] = lineArr[1];
		installedPackageReader.close();
		return installedPackageDict;

	def installPackageByPip(self, obj, packageName, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system(pythonPath.replace("\\", "/") + "/Scripts/pip.exe install " + packageName) == 0:
				return True;
		else:
			if os.system("pip install " + packageName) == 0:
				return True;
		return False;

	def updatePipVersion(self, obj, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system(pythonPath.replace("\\", "/") + "/Scripts/python.exe -m pip install --upgrade pip") == 0:
				return True;
		else:
			if os.system("python -m pip install --upgrade pip") == 0:
				return True;
		return False;

	def checkPackageIsInstalled(self, obj, packageName, pythonPath = None, _retTuple = None):
		isInstalled = False
		try:
			imp.find_module(packageName);
			isInstalled = True;
		except Exception:
			isInstalled = False;
		return isInstalled;

	def installPipByEasyInstall(self, obj, pythonPath = None, _retTuple = None):
		_GG("Log").i(pythonPath);
		if pythonPath and len(pythonPath) > 0:
			if os.system(pythonPath.replace("\\", "/") + "/Scripts/easy_install.exe pip") == 0:
				return True;
		else:
			if os.system("easy_install pip") == 0:
				return True;
		return False;