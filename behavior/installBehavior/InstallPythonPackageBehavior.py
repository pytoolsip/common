# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-04-23 22:18:59
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-16 15:09:24

import re;
import os;
import imp;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName",
	};

def __getExposeMethod__(DoType):
	return {
		"getInstalledPackagesByPip" : DoType.AddToRear,
		"installPackageByPip" : DoType.AddToRear,
		"updatePipVersion" : DoType.AddToRear,
		"checkPackageIsInstalled" : DoType.AddToRear,
		"uninstallPackageByPip" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		{
			"path" : "ConfigParseBehavior/JsonConfigBehavior", 
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
	];

class InstallPythonPackageBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(InstallPythonPackageBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = InstallPythonPackageBehavior.__name__;
		pass;

	# 获取已通过pip安装的包
	def getInstalledPackagesByPip(self, obj, pythonPath = None, _retTuple = None):
		installedPackageDict = {};
		if pythonPath:
			installedPackageReader = os.popen(os.path.abspath(os.path.join(pythonPath, "python.exe")) + " -m pip freeze");
		else:
			installedPackageReader = os.popen("pip freeze");
		installedPackageLines = installedPackageReader.read();
		for line in installedPackageLines.splitlines():
			lineArr = line.split("==");
			if len(lineArr) == 2:
				installedPackageDict[lineArr[0]] = lineArr[1];
		installedPackageReader.close();
		return installedPackageDict;

	def installPackageByPip(self, obj, packageName, version = "", pythonPath = None, _retTuple = None):
		cmd = self.getPipInstallCmd(obj, packageName, version = "", pythonPath = pythonPath);
		if os.system(cmd) == 0:
			return True;
		return False;

	def updatePipVersion(self, obj, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system(os.path.abspath(os.path.join(pythonPath, "python.exe")) + " -m pip install --upgrade pip") == 0:
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
			pkgDict = obj.getInstalledPackagesByPip(pythonPath = pythonPath);
			if packageName in pkgDict:
				isInstalled = True;
		return isInstalled;

	def uninstallPackageByPip(self, obj, packageName, pythonPath = None, _retTuple = None):
		if pythonPath:
			if os.system(os.path.abspath(os.path.join(pythonPath, "python.exe")) + f" -m pip uninstall {packageName} -y") == 0:
				return True;
		else:
			if os.system(f"pip uninstall {packageName} -y") == 0:
				return True;
		return False;
	
	def getPipInstallImage(self, obj):
		if os.path.exists(_GG("g_DataPath")+"config/setting_cfg.json"):
			cfg = obj.readJsonFile(_GG("g_DataPath")+"config/setting_cfg.json");
			if cfg:
				return cfg.get("pip_install_image", "");
		return "";
	
	def getPipInstallCmd(self, obj, packageName, version = "", pythonPath = None):
		cmd = "pip install " + packageName;
		if version:
			cmd += f"=={version}";
		if pythonPath:
			cmd = os.path.abspath(os.path.join(pythonPath, "python.exe")) + " -m pip install " + packageName;
		# 获取镜像
		pii = self.getPipInstallImage(obj);
		if pii:
			cmd += f" -i {pii}";
			mtObj = re.match("^https?://(.*)/.*$", pii);
			if mtObj:
				host = mtObj.group(1);
				cmd += f" --trusted-host {host}";
		return cmd;