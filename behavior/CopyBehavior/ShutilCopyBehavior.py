# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-29 22:06:46
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-16 15:09:23

import os;
import shutil;

from _Global import _GG;
from function.base import *;
BaseBehavior = _GG("BaseBehavior");

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"copyPath" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class ShutilCopyBehavior(BaseBehavior):
	def __init__(self):
		super(ShutilCopyBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = ShutilCopyBehavior.__name__;
		pass;

	# 拷贝路径方法【obj为绑定该组件的对象，_retTuple为该组件的前个函数返回值】
	def copyPath(self, obj, srcPath, dstPath, _retTuple = None):
		# 校验传入的参数
		if isinstance(srcPath, str) and isinstance(dstPath, str):
			# 判断要拷贝的文件是否存在
			if os.path.exists(srcPath):
				# 判断索要拷贝的是文件还是文件夹
				if os.path.isfile(srcPath):
					shutil.copyfile(srcPath, dstPath);
					return True;
				elif os.path.isdir(srcPath):
					shutil.copytree(srcPath, dstPath);
					return True;
				else:
					_GG("Log").w("The source path named '" + srcPath + "' is not file or dir !!");
			else:
				_GG("Log").w("There is not source path named '" + srcPath + "' !!");
		return False;
