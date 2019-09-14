# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-07 20:34:55
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-07 20:34:55
import os,shutil,re,wx;
import compileall;
import threading;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"_copyProject_" : DoType.AddToRear,
		"_compileDir_" : DoType.AddToRear,
		"_compileProject_" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class CompilePyBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(CompilePyBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = CompilePyBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	# 拷贝工程
	def _copyProject_(self, obj, sPath, tPath, callback = None, callbackParams = {}, _retTuple = None):
		if not os.path.exists(tPath):
			os.makedirs(tPath);
		for name in os.listdir(sPath):
			# 过滤git文件
			if re.search("^\.git.*", os.path.basename(name)):
				continue;
			# 拼接地址
			srcPath = os.path.join(sPath, name);
			targetPath = os.path.join(tPath, name);
			if os.path.basename(name) in ["assets", "common", "update"]:
				self._copyProject_(obj, srcPath, targetPath, callback, callbackParams);
				continue;
			if callable(callback):
				callback(srcPath, callbackParams);
			if os.path.isfile(srcPath):
				shutil.copyfile(srcPath, targetPath);
			else:
				shutil.copytree(srcPath, targetPath);
		pass;

	# 编码路径下的py文件
	def _compileDir_(self, obj, dirPath, isRemoveOri = True, callback = None, _retTuple = None):
		compileall.compile_dir(dirPath);
		if callable(callback):
			callback(dirPath);
		if isRemoveOri:
			# 移动dirPath下__pycache__里的文件，并移除py文件
			for root, dirs, files in os.walk(dirPath):
				for path in dirs:
					if os.path.basename(path) != "__pycache__":
						continue;
					pycachePath = os.path.join(root,path);
					for name in os.listdir(pycachePath):
						fPath = os.path.join(pycachePath,name);
						if os.path.isfile(fPath):
							# 重命名文件
							mtObj = re.match("^(.*)\..*(\..*)$", name);
							if mtObj:
								newName = "".join(mtObj.groups());
								newFPath = os.path.join(pycachePath,newName);
								os.rename(fPath, newFPath);
								fPath = newFPath;
							# 移动文件
							shutil.move(fPath, os.path.join(pycachePath, ".."));
					# 删除__pycache__文件夹
					shutil.rmtree(pycachePath);
				for name in files:
					if name.endswith(".py"):
						os.remove(os.path.join(root,name));
		pass;

	# 编码工程
	def _compileProject_(self, obj, sPath, tPath, isRemoveOri = True, finishCallback = None, _retTuple = None):
		if not os.path.exists(sPath):
			return;
		if not os.path.exists(tPath):
			os.makedirs(tPath);
		proDialog = wx.ProgressDialog("编码工程", "", style = wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME|wx.PD_ESTIMATED_TIME|wx.PD_REMAINING_TIME|wx.PD_AUTO_HIDE);
		def updateProDialog(value, info):
			value = proDialog.GetRange() * value;
			if value >= proDialog.GetRange():
				wx.CallAfter(proDialog.Update, proDialog.GetRange(), "已完成工程编码，路径为：\n" + str(tPath));
			else:
				wx.CallAfter(proDialog.Update, value, info);
		# 开始编码工程
		def compileProject(srcPath, tgtPath, isRemoveOri, callback, finishCallback):
			# 拷贝工程
			callback(0, "开始拷贝工程\n" + str(srcPath));
			def copyCallback(path, params):
				updateProDialog(params["curVal"], "正在拷贝工程\n" + str(path));
				params["count"] += 1;
				params["curVal"] = params["process"] * params["count"]/100;
				if params["curVal"] > params["process"]:
					params["curVal"] = params["process"];
			self._copyProject_(obj, sPath, tPath, callback = copyCallback, callbackParams = {"count":0, "curVal":0, "process":0.5});
			# 编码工程
			callback(0.5, "开始编码对应路径\n" + str(tgtPath));
			def compileCallback(dirPath):
				callback(0.75, "完成对应路径的编码\n" + str(dirPath));
				if isRemoveOri:
					callback(0.75, "移除相应路径的py文件\n" + str(dirPath));
			self._compileDir_(obj, tgtPath, isRemoveOri = isRemoveOri, callback = compileCallback);
			callback(1, "");
			# 回调结束方法
			if callable(finishCallback):
				wx.CallAfter(finishCallback, tgtPath);
			pass;
		threading.Thread(target = compileProject, args = (sPath, tPath, isRemoveOri, updateProDialog, finishCallback)).start();
		proDialog.Update(0, "开始编码\n" + str(sPath));
		proDialog.ShowModal();
		pass;