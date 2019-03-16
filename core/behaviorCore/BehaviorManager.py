# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-08-25 03:33:52
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:54:25

from behaviorCore.BehaviorBinder import BehaviorBinder;

from _Global import _GG;
from function.base import *;

# 扩展方法到对象
def ExtendMethodToObj(obj, methodName, method):
	if callable(method):
		def newMethod(*argList, **argDict):
			method(obj, *argList, **argDict);
		setattr(obj, methodName, newMethod);

class BehaviorManager(object):
	def __init__(self):
		super(BehaviorManager, self).__init__();
		self._className_ = BehaviorManager.__name__;
		self.__behaviorBinder__ = BehaviorBinder();
		self.__behaviorPathMap__ = {}; # 组件路径映射表

	# 根据相对路径require组件实例
	def requireBehavior(self, path, basePath = None):
		try:
			bhPath = path;
			if basePath:
				bhPath = GetPathByRelativePath(path, basePath);
			if bhPath not in self.__behaviorPathMap__:
				behaviorPathList = bhPath.split("/");
				behaviorFileName = behaviorPathList.pop();
				# 获取组件实例，并设置组件属性
				behavior = require("/".join(behaviorPathList), behaviorFileName, behaviorFileName)();
				bid = _GG("getUniqueId")(); # 组件实例的唯一ID
				behavior.setBehaviorId("behavior_" + str(bid)); # 设置组件的唯一ID
				behavior.setBehaviorPath(bhPath); # 设置组件的路径
				self.__behaviorPathMap__[bhPath] = bid;
				return behavior;
			else:
				_GG("Log").w("Require behavior fail! Because of binded behavior[{}] !".format(bhPath));
		except Exception as e:
			_GG("Log").w("Require behavior fail! [{}] =>".format(path), e);
		return None;

	# 根据组件配置require组件实例
	def requireBehaviorByConfig(self, behaviorConfig):
		behavior = None;
		if isinstance(behaviorConfig, _GG("BaseBehavior")):
			if hasattr(behaviorConfig, "behaviorId_"):
				behavior = behaviorConfig;
			else:
				_GG("Log").w("Bind behavior fail ! Because of no behaviorId_ .");
		elif isinstance(behaviorConfig, str):
			behavior = self.requireBehavior(behaviorConfig);
		elif isinstance(behaviorConfig, dict):
			requireFunc = self.requireBehavior;
			if "require" in behaviorConfig:
				requireFunc = behavior["require"];
			if "path" in behaviorConfig:
				basePath = "";
				if "basePath" in behaviorConfig:
					basePath = behaviorConfig["basePath"];
				behavior = requireFunc(behaviorConfig["path"], basePath = basePath);
				if behavior:
					# 设置组件ID
					if not hasattr(behavior, "behaviorId_"):
						bid = _GG("getUniqueId")(); # 组件的唯一ID
						behavior.setBehaviorId("behavior_" + str(bid)); # 设置组件的唯一ID
					# 设置组件名称
					if "name" in behaviorConfig:
						behavior.setBehaviorName(behaviorConfig["name"]);
		return behavior;

	# 绑定组件
	def bindBehavior(self, obj, behaviorConfig):
		behavior = None;
		try:
			# 根据组件配置require组件实例
			behavior = self.requireBehaviorByConfig(behaviorConfig);
			# 初始化所绑定组件实例保存到对象的字段
			if not hasattr(obj, "_BEHAVIOR_DICT_"):
				obj._BEHAVIOR_DICT_ = {};
			# 绑定组件【绑定前需判断是否已绑定】
			if behavior:
				if behavior.getBehaviorId() not in obj._BEHAVIOR_DICT_:
					self.bindDependBehaviors(obj, behavior); # 绑定依赖组件
					self.__behaviorBinder__.bindBehaviorToObj(behavior, obj); # 绑定组件到对象上
					# 保存所绑定组件实例到对象的_BEHAVIOR_DICT_
					obj._BEHAVIOR_DICT_[behavior.getBehaviorId()] = behavior;
				else:
					_GG("Log").w("Bind behavior fail ! Because of binded behavior[name:{},id:{}] in obj .".format(behavior.getBehaviorName(), behavior.getBehaviorId()));
		except Exception as e:
			_GG("Log").w("Bind behavior fail! [{}] =>".format(behaviorConfig), e);
		return behavior;

	# 解绑组件
	def unbindBehavior(self, obj, behavior):
		try:
			if isinstance(behavior, _GG("BaseBehavior")):
				self.unbindDependBehaviors(obj, behavior);
				self.__behaviorBinder__.unbindBehaviorToObj(behavior, obj);
				return True;
			else:
				_GG("Log").w("UnBind behavior[name:{},id:{}] fail ! Because behavior is not base on BaseBehavior .".format(behavior.getBehaviorName()));
		except Exception as e:
			_GG("Log").w("UnBind behavior fail! =>", e);
		return False;

	# 绑定依赖组件
	def bindDependBehaviors(self, obj, behavior):
		if hasattr(behavior, "_DEPEND_BEHAVIOR_LIST_") and isinstance(behavior._DEPEND_BEHAVIOR_LIST_, list):
			for i in range(len(behavior._DEPEND_BEHAVIOR_LIST_)):
				dependBehavior = self.bindBehavior(obj, behavior._DEPEND_BEHAVIOR_LIST_[i]);
				if dependBehavior:
					# 保存被依赖组件索引
					if not hasattr(dependBehavior, "_BE_DEPENDED_BEHAVIOR_LIST_"):
						dependBehavior._BE_DEPENDED_BEHAVIOR_LIST_ = [];
					dependBehavior._BE_DEPENDED_BEHAVIOR_LIST_.append(behavior.behaviorId_);
					# 重置依赖组件
					behavior._DEPEND_BEHAVIOR_LIST_[i] = dependBehavior;

	# 解绑依赖组件
	def unbindDependBehaviors(self, obj, behavior):
		if hasattr(behavior, "_DEPEND_BEHAVIOR_LIST_") and isinstance(behavior._DEPEND_BEHAVIOR_LIST_, list):
			for i in range(len(behavior._DEPEND_BEHAVIOR_LIST_)-1, -1, -1):
				dependBehavior = behavior._DEPEND_BEHAVIOR_LIST_[i];
				# 删除被依赖组件索引
				if hasattr(dependBehavior, "_BE_DEPENDED_BEHAVIOR_LIST_") and behavior.behaviorId_ in dependBehavior._BE_DEPENDED_BEHAVIOR_LIST_:
					behaviorIdx = dependBehavior._BE_DEPENDED_BEHAVIOR_LIST_.index(behavior.behaviorId_);
					dependBehavior._BE_DEPENDED_BEHAVIOR_LIST_.pop(behaviorIdx);
					# 如果被依赖组件列表为空，则解绑对应的依赖组件
					if len(dependBehavior._BE_DEPENDED_BEHAVIOR_LIST_) == 0:
						self.unbindBehavior(obj, dependBehavior)
				# 删除依赖组件索引
				behavior._DEPEND_BEHAVIOR_LIST_.pop(i);

	# 根据组件ID获取组件
	def getBehaviorById(self, obj, behaviorId):
		if hasattr(obj, "_BEHAVIOR_DICT_") and behaviorId in obj._BEHAVIOR_DICT_:
			return obj._BEHAVIOR_DICT_[behaviorId];

	# 根据组件名称获取组件列表
	def getBehaviorsByName(self, obj, name):
		behaviors = [];
		if hasattr(obj, "_BEHAVIOR_DICT_"):
			for behaviorId in obj._BEHAVIOR_DICT_:
				if obj._BEHAVIOR_DICT_[behaviorId].getBehaviorName() == name:
					behaviors.append(obj._BEHAVIOR_DICT_[behaviorId]);
		return behaviors;

	# 根据组件路径获取组件列表
	def getBehaviorsByPath(self, obj, path):
		behaviors = [];
		if hasattr(obj, "_BEHAVIOR_DICT_"):
			for behaviorId in obj._BEHAVIOR_DICT_:
				if obj._BEHAVIOR_DICT_[behaviorId].getBehaviorPath() == path:
					behaviors.append(obj._BEHAVIOR_DICT_[behaviorId]);
		return behaviors;

	# 扩展组件相关操作方法到对象
	def extendBehavior(self, obj):
		methodNameList = [
			"bindBehavior",
			"unbindBehavior",
			"getBehaviorById",
			"getBehaviorsByName",
			"getBehaviorsByPath",
		];
		for methodName in methodNameList:
			ExtendMethodToObj(obj, methodName, getattr(self, methodName));
