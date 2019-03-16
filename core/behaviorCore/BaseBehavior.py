# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-24 12:24:07
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:28

from enum import Enum, unique;
from _Global import _GG;

# 枚举执行类型
@unique
class DoType(Enum):
	AddToFront = 0; # 前置添加
	Override = 1; # 覆盖/覆写
	AddToRear = 2; # 后置添加

class BaseBehavior(object):
	def __init__(self, depends = [], exposeData = {}, exposeMethod = None):
		super(BaseBehavior, self).__init__();
		self._className_ = BaseBehavior.__name__;
		self._DEPEND_BEHAVIOR_LIST_ = depends; # 依赖组件列表
		self._BE_DEPENDED_BEHAVIOR_LIST_ = []; # 被依赖组件列表
		self.__EXPOSE_DATA__ = exposeData; # 导出数据
		self.__EXPOSE_METHOD__ = exposeMethod; # 导出方法

	# 打印obj绑定的组件名称【obj为绑定该组件的对象，argList和argDict为可变参数】
	def printBehaviorName(self, obj, *argList, **argDict):
		_GG("Log").i(self.getBehaviorName());
		pass;

	# 设置组件Id
	def setBehaviorId(self, bid):
		self.behaviorId_ = bid;

	# 获取组件Id
	def getBehaviorId(self):
		return self.behaviorId_;

	# 设置组件名称
	def setBehaviorName(self, name):
		self.__behaviorName__ = name;

	# 获取组件路径
	def getBehaviorName(self):
		if hasattr(self, "__behaviorName__"):
			return self.__behaviorName__;
		return self._className_;

	# 设置组件路径
	def setBehaviorPath(self, path):
		self.__behaviorPath__ = path;

	# 获取组件路径
	def getBehaviorPath(self):
		if hasattr(self, "__behaviorPath__"):
			return self.__behaviorPath__;
		return "";

	# 获取组件导出数据
	def getBehaviorExposeData(self):
		baseExposeData = {};
		exposeData = self.__EXPOSE_DATA__; # 获取暴露出的数据
		for dataKey,dataValue in baseExposeData.items():
			if dataKey not in exposeData:
				exposeData[dataKey] = dataValue;
		return exposeData;

	# 获取组件导出方法
	def getBehaviorExposeMethod(self):
		baseExposeMethod = {"printBehaviorName" : DoType.AddToRear};
		exposeMethod = callable(self.__EXPOSE_METHOD__) and self.__EXPOSE_METHOD__(DoType) or {}; # 获取暴露出的方法接口
		for methodName,methodType in baseExposeMethod.items():
			if methodName not in exposeMethod:
				exposeMethod[methodName] = methodType;
		return exposeMethod;