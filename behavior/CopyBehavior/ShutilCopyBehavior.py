# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-29 22:06:46
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-10-29 22:37:18

import os;
import shutil;

from _Global import _GG;
from function.base import *;
BaseBehavior = _GG("BaseBehavior");

def getExposeData():
	return {
		# "exposeDataName" : {},
	};

def getExposeMethod(DoType):
	return {
		"copyPath" : DoType.AddToRear,
	};

class ShutilCopyBehavior(BaseBehavior):
	def __init__(self, depends = []):
		super(ShutilCopyBehavior, self).__init__(depends);
		self.className_ = ShutilCopyBehavior.__name__;
		pass;

	def getExposeData(self):
		return getExposeData(); # 获取暴露出的数据

	def getExposeMethod(self, DoType):
		return getExposeMethod(DoType); # 获取暴露出的方法接口

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
					print("The source path named '" + srcPath + "' is not file or dir !!");
			else:
				print("There is not source path named '" + srcPath + "' !!");
		return False;
