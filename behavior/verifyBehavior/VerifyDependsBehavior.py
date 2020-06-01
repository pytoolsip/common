# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-08-24 19:15:38
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-05-21 17:20:51
import wx;
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
		"_dealDependMap_" : DoType.AddToRear,
		"_getDependMap_" : DoType.AddToRear,
		"_saveDependMap_" : DoType.AddToRear,
		"_checkDependMods_" : DoType.AddToRear,
		"_uninstallDependMods_" : DoType.AddToRear,
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
		modList, modFile = [], os.path.abspath(os.path.join(assetsPath, "depends.mod"));
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
				rmModList.append((mod, ver));
		for mod, ver in tgtModList:
			if mod not in srcModMap or (ver and not srcModMap[mod]):
				addModList.append((mod, ver));
			elif ver and srcModMap[mod] and ver != srcModMap[mod]:
				return False, addModList, rmModList;
		return True, addModList, rmModList;

	# 处理依赖模块表
	def _dealDependMap_(self, obj, tkey, srcPath, targetPath, pythonPath, onInstall = None, onUninstall = None, onFinish = None, _retTuple = None):
		dependMap = self._getDependMap_(obj);
		ret, addModList, rmModList = self._diffDependMods_(obj, srcPath, targetPath);
		if ret:
			curIdx, totalCnt = 0, len(addModList) + len(rmModList);
			def installCallback(mod):
				onInstall(mod, curIdx/totalCnt);
			for mod, ver in addModList:
				isInstallMod = self._addDependMod_(obj, tkey, mod, version = ver, pythonPath = pythonPath, dependMap = dependMap, callback = installCallback);
				# 调用安装回调
				curIdx += 1;
				if isInstallMod and callable(onInstall):
					onInstall(mod, curIdx/totalCnt, isEnd = True);
			def uninstallCallback(mod):
				onUninstall(mod, curIdx/totalCnt);
			for mod, ver in rmModList:
				isUninstallMod = self._removeDependMod_(obj, tkey, mod, pythonPath = pythonPath, dependMap = dependMap, callback = uninstallCallback);
				# 调用卸载回调
				curIdx += 1;
				if isUninstallMod and callable(onUninstall):
					onUninstall(mod, curIdx/totalCnt, isEnd = True);
			if totalCnt > 0:
				wx.CallAfter(obj._saveDependMap_, dependMap);
		# 成功回调
		if callable(onFinish):
			onFinish(ret);
		return ret;

	def _getDependMap_(self, obj, _retTuple = None):
		dependMapFile = _GG("g_DataPath") + "depend_map.json";
		return self.__getJsonData__(dependMapFile);

	def _saveDependMap_(self, obj, dependMap, _retTuple = None):
		dependMapFile = _GG("g_DataPath") + "depend_map.json";
		with open(dependMapFile, "w") as f:
			f.write(json.dumps(dependMap));

	def _checkDependMods_(self, obj, dependsPath, isAllowMiss = False, _retTuple = None):
		dependMap = self._getDependMap_(obj);
		modList = self._getDependMods_(obj, dependsPath);
		for mod, ver in modList:
			if mod in dependMap:
				dVer = dependMap[mod].get("ver", "");
				if not dVer or not ver or dVer == ver:
					continue;
				return False;
			elif not isAllowMiss:
				return False;
		return True;

	def _addDependMod_(self, obj, tkey, mod, version = "", pythonPath = None, dependMap = None, callback = None, _retTuple = None):
		isSaveNow = not isinstance(dependMap, dict);
		if isSaveNow:
			dependMap = self._getDependMap_(obj);
		isInstall = False;
		depend = dependMap.get(mod, {});
		if depend:
			if depend["ver"]:
				if version and version != depend["ver"]:
					return False;
			elif version:
				if callable(callback):
					callback(mod);
				obj.installPackageByPip(mod, version = version, pythonPath = pythonPath);
				depend["ver"] = version;
				isInstall = True;
			depend["map"][tkey] = version;
		else:
			if callable(callback):
				callback(mod);
			obj.installPackageByPip(mod, version = version, pythonPath = pythonPath);
			dependMap[mod] = {
				"ver" : version,
				"map" : {
					tkey : version,
				},
			};
			isInstall = True;
		if isSaveNow:
			wx.CallAfter(obj._saveDependMap_, dependMap);
		return isInstall;

	def _removeDependMod_(self, obj, tkey, mod, pythonPath = None, dependMap = None, callback = None, _retTuple = None):
		isSaveNow = not isinstance(dependMap, dict);
		if isSaveNow:
			dependMap = self._getDependMap_(obj);
		isUninstall = False;
		depend = dependMap.get(mod, {});
		if depend:
			if tkey in depend["map"]:
				version = depend["map"][tkey];
				depend["map"].pop(tkey);
				if version and version == depend["ver"]:
					depend["ver"] = "";
					for ver in depend["map"].values():
						if ver:
							depend["ver"] = ver;
			if not depend["map"]:
				if callable(callback):
					callback(mod);
				obj.uninstallPackageByPip(mod, pythonPath = pythonPath);
				dependMap.pop(mod);
				isUninstall = True;
			if isSaveNow:
				wx.CallAfter(obj._saveDependMap_, dependMap);
		return isUninstall;

	# 卸载工具依赖模块
	def _uninstallDependMods_(self, obj, tkey, assetsPath, pythonPath = None, onUninstall = None, onFinish = None, _retTuple = None):
		dependMap = self._getDependMap_(obj);
		modList = self._getDependMods_(obj, assetsPath);
		curIdx, totalCnt = 0, len(modList);
		def uninstallCallback(mod):
			onUninstall(mod, curIdx/totalCnt);
		for mod, ver in modList:
			isUninstallMod = self._removeDependMod_(obj, tkey, mod, pythonPath = pythonPath, dependMap = dependMap, callback = uninstallCallback);
			# 调用卸载回调
			curIdx += 1;
			if isUninstallMod and callable(onUninstall):
				onUninstall(mod, curIdx/totalCnt, isEnd = True);
		if totalCnt > 0:
			wx.CallAfter(obj._saveDependMap_, dependMap);
		# 完成回调
		if callable(onFinish):
			onFinish();