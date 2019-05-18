# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-21 22:31:37
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 19:05:07

import sys;
import os;
import re;
import time;

# 动态加载模块
def require(filePath, moduleName, subModuleName = None, isReload = False, isReserve = False, modulePathBase = ""):
	modulePath = "/".join([filePath, moduleName]).replace("\\", "/");
	# 判断是否重新加载模块
	if isReload and modulePath in sys.modules:
		oldModule = sys.modules.pop(modulePath);
		if isReserve:
			sys.modules[modulePath+"_"+str(time.time())] = oldModule;
	# 判断缓存中是否已存在模块
	module = sys.modules.get(modulePath, None);
	if not module:
		# 拷贝sys.modules
		oriMods = {};
		for k,v in sys.modules.items():
			oriMods[k] = v;
		# 加载模块
		sys.path.insert(0, filePath);
		module = __import__(moduleName);
		sys.path.remove(filePath);
		# 恢复sys.modules
		popKList = [];
		for k in sys.modules.keys():
			if k in oriMods:
				sys.modules[k] = oriMods[k];
			elif modulePathBase and VerifyPath(modulePathBase) not in VerifyPath(k):
				popKList.append(k);
		for k in popKList:
				sys.modules.pop(k);
		# 添加缓存模块的key值
		sys.modules[modulePath] = module;
	# 获取子模块
	if subModuleName:
		return getattr(module, subModuleName);
	return module;

# 获取相对路径
def GetPathByRelativePath(path, basePath = ""):
	if len(basePath) == 0:
		basePath = os.getcwd();
	basePath = re.sub(r"\\", r"/", basePath);
	basePathList = basePath.split("/");
	if len(basePathList[-1]) == 0:
		basePathList.pop();
	path = re.sub(r"\\", r"/", path);
	pathList = path.split("/");
	if pathList[0] == ".":
		pathList.pop(0);
	while len(pathList) > 0:
		if pathList[0] == "..":
			basePathList.pop();
			pathList.pop(0);
		else:
			basePathList.extend(pathList);
			break;
	return "/".join(basePathList).strip();

# 创建控制类（视图或窗口）
def CreateCtr(path, parent, params = {}, isReload = False, isReserve = False, modulePathBase = ""):
	path = re.sub(r"\\", r"/", path);
	if path[-1] == "/":
		path = path[:-1];
	ctrName = path.split("/")[-1] + "Ctr";
	Ctr = require(path, ctrName, ctrName, isReload, isReserve, modulePathBase = modulePathBase);
	return Ctr(parent, params = params);

# 销毁控制类【需先销毁UI】（视图或窗口）
def DelCtr(ctr):
	Del(ctr.getUI());
	Del(ctr);

# 主动销毁类
def Del(obj):
	if hasattr(obj, "__dest__"):
		obj.__dest__();
	del obj;

# 校验路径
def VerifyPath(path):
	if sys.platform.startswith("win32"):
		return path.replace("/", "\\");
	else:
		return path.replace("\\", "/");