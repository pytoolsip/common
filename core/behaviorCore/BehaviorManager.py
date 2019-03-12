# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-08-25 03:33:52
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-23 14:25:50

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
		self.className_ = BehaviorManager.__name__;
		self.BehaviorBinder = BehaviorBinder();
		pass;

	# 根据相对路径require组件实例
	def requireBehaviorByPath(self, path, basePath = None):
		try:
			bhPath = path;
			if basePath:
				bhPath = GetPathByRelativePath(path, basePath);
			behaviorPathList = bhPath.split("\\");
			behaviorFileName = behaviorPathList.pop();
			behaviorObj = require("\\".join(behaviorPathList), behaviorFileName, behaviorFileName);
			return behaviorObj();
		except Exception as e:
			print("Require behavior fail! =>", e);

	# require组件实例
	def requireBehavior(self, path, basePath = None):
		behavior = self.requireBehaviorByPath(path, basePath = basePath);
		bid = _GG("getUniqueId")(); # 组件的唯一ID
		behavior.setBehaviorId("behavior_" + str(bid)); # 设置组件的唯一ID
		behavior.setBehaviorPath(path); # 设置组件的路径
		return behavior;

	# 根据组件配置require组件实例
	def requireBehaviorByConfig(self, behaviorConfig):
		behavior = None;
		if isinstance(behaviorConfig, _GG("BaseBehavior")):
			if hasattr(behaviorConfig, "behaviorId_"):
				behavior = behaviorConfig;
			else:
				print("Bind behavior fail ! Because of no behaviorId_ .");
		elif isinstance(behaviorConfig, str):
			behavior = self.requireBehavior(behaviorConfig);
			if not hasattr(behavior, "behaviorId_"):
				bid = _GG("getUniqueId")(); # 组件的唯一ID
				behavior.setBehaviorId("behavior_" + str(bid)); # 设置组件的唯一ID
		elif isinstance(behaviorConfig, dict):
			requireFunc = self.requireBehavior;
			if "require" in behaviorConfig:
				requireFunc = behavior["require"];
			if "path" in behaviorConfig:
				basePath = "";
				if "basePath" in behaviorConfig:
					basePath = behaviorConfig["basePath"];
				behavior = requireFunc(behaviorConfig["path"], basePath = basePath);
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
			if not hasattr(obj, "behaviorDict__"):
				obj.behaviorDict__ = {};
			# 绑定组件【绑定前需判断是否已绑定】
			if behavior:
				if behavior.getBehaviorId() not in obj.behaviorDict__:
					self.bindDependBehaviors(obj, behavior); # 绑定依赖组件
					self.BehaviorBinder.bindBehaviorToObj(behavior, obj); # 绑定组件到对象上
					# 保存所绑定组件实例到对象的behaviorDict__
					obj.behaviorDict__[behavior.getBehaviorId()] = behavior;
				else:
					print("Bind behavior fail ! Because of existing behavior[{}] in obj .".format(behavior.getBehaviorId()));
			else:
				print("Bind behavior fail ! Because of failing to require behavior by param : {} .".format(behaviorConfig));
		except Exception as e:
			print("Bind behavior fail! =>", e);
		return behavior;

	# 解绑组件
	def unbindBehavior(self, obj, behavior):
		try:
			if isinstance(behavior, _GG("BaseBehavior")):
				self.unbindDependBehaviors(obj, behavior);
				self.BehaviorBinder.unbindBehaviorToObj(behavior, obj);
				return True;
			else:
				print("UnBind behavior fail ! Because behavior is not base on BaseBehavior .");
		except Exception as e:
			print("UnBind behavior fail! =>", e);
		return False;

	# 绑定依赖组件
	def bindDependBehaviors(self, obj, behavior):
		if hasattr(behavior, "DependBehaviorList_") and isinstance(behavior.DependBehaviorList_, list):
			for i in range(len(behavior.DependBehaviorList_)):
				dependBehavior = self.bindBehavior(obj, behavior.DependBehaviorList_[i]);
				if dependBehavior:
					# 保存被依赖组件索引
					if not hasattr(dependBehavior, "BeDependedBehaviorList_"):
						dependBehavior.BeDependedBehaviorList_ = [];
					dependBehavior.BeDependedBehaviorList_.append(behavior.behaviorId_);
					# 重置依赖组件
					behavior.DependBehaviorList_[i] = dependBehavior;

	# 解绑依赖组件
	def unbindDependBehaviors(self, obj, behavior):
		if hasattr(behavior, "DependBehaviorList_") and isinstance(behavior.DependBehaviorList_, list):
			for i in range(len(behavior.DependBehaviorList_)-1, -1, -1):
				dependBehavior = behavior.DependBehaviorList_[i];
				# 删除被依赖组件索引
				if hasattr(dependBehavior, "BeDependedBehaviorList_") and behavior.behaviorId_ in dependBehavior.BeDependedBehaviorList_:
					behaviorIdx = dependBehavior.BeDependedBehaviorList_.index(behavior.behaviorId_);
					dependBehavior.BeDependedBehaviorList_.pop(behaviorIdx);
					# 如果被依赖组件列表为空，则解绑对应的依赖组件
					if len(dependBehavior.BeDependedBehaviorList_) == 0:
						self.unbindBehavior(obj, dependBehavior)
				# 删除依赖组件索引
				behavior.DependBehaviorList_.pop(i);

	# 根据组件ID获取组件
	def getBehaviorById(self, obj, behaviorId):
		if hasattr(obj, "behaviorDict__") and behaviorId in obj.behaviorDict__:
			return obj.behaviorDict__[behaviorId];

	# 根据组件名称获取组件列表
	def getBehaviorsByName(self, obj, name):
		behaviors = [];
		if hasattr(obj, "behaviorDict__"):
			for behaviorId in obj.behaviorDict__:
				if obj.behaviorDict__[behaviorId].getBehaviorName() == name:
					behaviors.append(obj.behaviorDict__[behaviorId]);
		return behaviors;

	# 根据组件路径获取组件列表
	def getBehaviorsByPath(self, obj, path):
		behaviors = [];
		if hasattr(obj, "behaviorDict__"):
			for behaviorId in obj.behaviorDict__:
				if obj.behaviorDict__[behaviorId].getBehaviorPath() == path:
					behaviors.append(obj.behaviorDict__[behaviorId]);
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
