# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-08-24 19:15:38
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-05-21 17:20:51
import os, json;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"_getDependMods_" : DoType.AddToRear,
		"_diffDependMods_" : DoType.AddToRear,
		"_checkDependMap_" : DoType.AddToRear,
		"_updateDependMap_" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		{
			"path" : "installBehavior/InstallPythonPackageBehavior", 
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
	];

class VerifyDependsBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(VerifyDependsBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = VerifyDependsBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	# 分割等号
	def __splitEqualSign__(self, modstr):
		modstr = modstr.strip();
		if modstr.find("=") != -1:
			if modstr.find("==") != -1:
				return tuple(modstr.split("=="));
			return tuple(modstr.split("="));
		return (modstr, "");

	# 转换mod格式
	def __convertModListToMap__(self, modList):
		modMap = {};
		for mod, ver in modList:
			modMap[mod] = ver;
		return modMap;

	# 获取json数据
	def __getJsonData__(self, filePath):
		if os.path.exists(filePath):
			with open(filePath, "r") as f:
				return json.loads(f.read());
		return {};

	# 获取依赖模块列表
	def _getDependMods_(self, obj, assetsPath, _retTuple = None):
		modList, modFile = [], os.path.join(assetsPath, "depends.mod");
		if not os.path.exists(modFile):
			return modList;
		with open(modFile, "r") as f:
			for line in f.readlines():
				mod = self.__splitEqualSign__(line);
				if mod not in modList:
					modList.append(mod);
		return modList;

	# 获取不同的依赖模块列表
	def _diffDependMods_(self, obj, srcPath, targetPath, _retTuple = None):
		addModList, rmModList = [], [];
		srcModList, tgtModList = self._getDependMods_(obj, srcPath), self._getDependMods_(obj, targetPath);
		srcModMap, tgtModMap = self.__convertModListToMap__(srcModList), self.__convertModListToMap__(tgtModList);
		for mod, ver in srcModList:
			if mod not in tgtModMap:
				rmModList.append(mod);
		for mod, ver in tgtModList:
			if mod not in srcModMap:
				addModList.append(mod);
			elif ver and srcModMap[mod] and ver != srcModMap[mod]:
				return False, addModList, rmModList;
		return True, addModList, rmModList;

	# 检测依赖模块表
	def _checkDependMap_(self, obj, srcPath, targetPath, dependMapFile, pythonPath, onInstall = None, onUninstall = None, onFinish = None, _retTuple = None):
		dependMap = self.__getJsonData__(dependMapFile);
		ret, addModList, rmModList = self._diffDependMods_(obj, srcPath, targetPath);
		if ret:
			curIdx, totalCnt = 0, len(addModList) + len(rmModList);
			for mod in addModList:
				isInstallMod = False;
				if dependMap.get(mod, 0) <= 0:
					if callable(onInstall):
						onInstall(mod, curIdx/totalCnt);
					obj.installPackageByPip(mod, pythonPath = pythonPath);
					dependMap[mod] = 0;
					isInstallMod = True;
				dependMap[mod] = dependMap.get(mod, 0) + 1;
				# 调用安装回调
				curIdx += 1;
				if isInstallMod and callable(onInstall):
					onInstall(mod, curIdx/totalCnt, isEnd = True);
			for mod in rmModList:
				isUninstallMod = False;
				dependMap[mod] = dependMap.get(mod, 0) - 1;
				if dependMap.get(mod, 0) <= 0:
					if callable(onUninstall):
						onUninstall(mod, curIdx/totalCnt);
					obj.uninstallPackageByPip(mod, pythonPath = pythonPath);
					dependMap.pop(mod);
					isUninstallMod = True;
				# 调用卸载回调
				curIdx += 1;
				if isUninstallMod and callable(onUninstall):
					onUninstall(mod, curIdx/totalCnt, isEnd = True);
		# 成功回调
		if callable(onFinish):
			onFinish(totalCnt > 0, dependMap, ret);
		return totalCnt > 0, dependMap;

	def _updateDependMap_(self, obj, dependMap, dependMapFile, _retTuple = None):
		with open(dependMapFile, "w") as f:
			f.write(json.dumps(dependMap));