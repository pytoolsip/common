# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-06 23:14:13
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2020-02-05 19:51:21
import os,re;
import shutil;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"requestUpdateIP" : DoType.AddToRear,
		"updateIP" : DoType.AddToRear,
		"autoLoginIP" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		{
			"path" : "serviceBehavior/UpDownloadBehavior",
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
		{
			"path" : "serviceBehavior/IPInfoBehavior",
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
	];

class ServiceBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(ServiceBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = ServiceBehavior.__name__;
		pass;

	# 请求更新平台信息
	def requestUpdateIP(self, obj, callback = None, _retTuple = None):
		resp = _GG("CommonClient").callService("UpdateIP", "UpdateIPReq", {"version" : _GG("ClientConfig").UrlConfig().GetIPVersion()}, asynCallback = callback);
		if resp and resp.code == 0:
			return True, resp.version;
		return False, "";

	def updateIP(self, obj, version, _retTuple = None):
		# 获取更新文件
		updateFile = self.getUpdateFile();
		if not os.path.exists(updateFile):
			return False;
		_, ext = os.path.splitext(updateFile);
		# 创建更新文件夹
		updateDir = _GG("g_DataPath")+"update";
		if not os.path.exists(updateDir):
			os.makedirs(updateDir);
		# 拷贝更新文件
		filePath = os.path.join(updateDir, "update_pytoolsip"+ext);
		if os.path.exists(filePath):
			os.remove(filePath);
		shutil.copyfile(updateFile, filePath);
		# 分发更新平台事件
		_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_APP_EVENT, {"version" : version, "updateFile" : filePath});

	# 自动登录平台
	def autoLoginIP(self, obj, _retTuple = None):
		# 根据时间戳，判断是否过期
		timeStamp, expire = obj.getIPInfoConfig("user", "time_stamp"), obj.getIPInfoConfig("user", "expire");
		if not timeStamp or float(time.time()) - float(timeStamp) > float(expire):
			obj.removeIPInfoConfig("user"); # 移除用户数据
			return;
		# 读取配置
		name, pwd = obj.getIPInfoConfig("user", "name"), obj.getIPInfoConfig("user", "pwd");
		if name and pwd:
			# 登录回调
			def onLogin(respData):
				if respData:
					if respData.code == 0:
						_GG("EventDispatcher").dispatch(_GG("EVENT_ID").LOGIN_SUCCESS_EVENT, {"userInfo" : respData.userInfo, "expire" : respData.expire});
					else:
						obj.removeIPInfoConfig("user"); # 移除用户数据
				pass;
			# 请求服务
			_GG("CommonClient").callService("Login", "LoginReq", {
				"name" : name,
				"pwd" : obj.encodeStrByPublicKey(pwd),
				"isAuto" : True,
			}, asynCallback = onLogin);

	# 获取更新文件
	def getUpdateFile(self):
		updatePath = os.path.join(_GG("g_AssetsPath"), "update");
		if not os.path.exists(updatePath):
			updatePath = os.path.join(_GG("g_ProjectPath"), "assets", "update");
		# 获取更新脚本文件
		for fileName in os.listdir(updatePath):
			filePath = os.path.join(updatePath, fileName);
			if os.path.isfile(filePath) and re.search(r"^update\.py.*$", fileName):
				return filePath;
		return "";
