# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-06 23:14:13
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-27 18:38:07
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
		"checkUpdateIP" : DoType.AddToRear,
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

	# 检测更新平台
	def checkUpdateIP(self, obj, _retTuple = None):
		resp = _GG("CommonClient").callService("UpdateIP", "UpdateIPReq", {"version" : _GG("AppConfig")["version"]});
		if resp and resp.code == 0:
			# 重置文件夹【会移除原有文件夹】
			dirPath, targetPath = _GG("g_DataPath")+"update/pytoolsip_temp", _GG("g_DataPath")+"update/pytoolsip";
			if os.path.exists(dirPath):
				shutil.rmtree(dirPath);
			os.mkdir(dirPath);
			# 下载解压文件
			isLast = False;
			def onComplete(filePath):
				if os.path.splitext(filePath) != ".zip":
					return;
				# 解压文件
				def afterUnzip():
					# 删除压缩文件
					os.remove(filePath);
					# 更新程序
					if isLast:
						_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_APP_EVENT, {
							"tempPath" : dirPath,
							"targetPath" : targetPath,
							"targetMd5Path" self.getTargetMd5Path(targetPath),
							"updateFile" : self.getUpdateFile(dirPath),
						});
				obj.unzipFile(filePath, os.path.dirname(filePath), finishCallback = afterUnzip);
				pass;
			def callbackFunc(status):
				if status == wx.ID_OK:
					for urlInfo in resp.urlList:
						filePath = os.path.join(urlInfo.path, os.path.basename(urlInfo.url));
						if not os.path.exists(filePath):
							obj.download(urlInfo.url, os.path.join(dirPath, filePath), urlInfo.totalSize, onComplete = onComplete); # 下载平台包
					isLast = True;
				else:
					_GG("EventDispatcher").dispatch(_GG("EVENT_ID").STOP_APP_EVENT, {}); # 停止App
			_GG("WindowObject").CreateMessageDialog("检测有更新版本，是否确认更新？", "检测平台版本", style = wx.OK|wx.ICON_QUESTION, callback = callbackFunc);

	# 自动登录平台
	def autoLoginIP(self, obj, _retTuple = None):
		# 根据时间戳，判断是否过期
		timeStamp, expire = obj.getIPInfoConfig("user", "time_stamp"), obj.getIPInfoConfig("user", "expire");
		if not timeStamp or float(time.time()) - float(timeStamp) > expire:
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

	# 更新update文件夹
	def getUpdateFile(self, dirPath):
		updatePath = os.path.join(dirPath, "update");
		if not os.path.exists(updatePath):
			return "";
		# 获取更新脚本文件
		for fileName in os.listdir(updatePath):
			filePath = os.path.join(updatePath, fileName);
			if os.path.isfile(filePath) and re.search(r"^update\.py.*$", fileName):
				return filePath;
		return "";

	# 更新update文件夹
	def getTargetMd5Path(self, dirPath):
		fileName = "_file_md5_map_.json";
		for path in [dirPath, _GG("g_AssetsPath")]:
			if os.path.exists(os.path.join(path, fileName)):
				return path;
		return "";

