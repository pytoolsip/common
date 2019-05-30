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
		resp = _GG("CommonClient").callService("UpdateIP", "UpdateIPReq", {"uid" : _GG("CommonClient").getUserId(), "version" : _GG("AppConfig")["version"]});
		if resp and not resp.isUpToDate:
			def onComplete(filePath):
				# 重置文件夹【会移除原有文件夹】
				dirPath = _GG("g_DataPath")+"update/pytoolsip/";
				if os.path.exists(dirPath):
					shutil.rmtree(dirPath);
				os.mkdir(dirPath);
				# 解压文件
				def afterUnzip():
					# 删除压缩文件
					os.remove(filePath);
					# 更新程序
					_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_APP_EVENT, {
						"updatePath" : dirPath,
						"updateFile" : self.checkAndUpdateScript(dirPath),
					});
				obj.unzipFile(filePath, dirPath, finishCallback = afterUnzip);
				pass;
			def updateIP():
				# 下载平台包
				filePath = os.path.join(_GG("g_DataPath"), "temp/", resp.url.split("/")[-1]);
				obj.download(resp.url, filePath, resp.totalSize, onComplete = onComplete);
			if resp.isAllowQuit:
				def callbackFunc(status):
					if status == wx.ID_YES:
						updateIP();
				_GG("WindowObject").CreateMessageDialog("检测有更新版本，是否确认更新？", "检测平台版本", style = wx.YES_NO|wx.ICON_QUESTION, callback = callbackFunc);
			else:
				_GG("WindowObject").CreateMessageDialog("检测有更新版本，是否确认更新？", "检测平台版本", style = wx.OK|wx.ICON_QUESTION);
				updateIP();

	# 自动登录平台
	def autoLoginIP(self, obj, _retTuple = None):
		# 根据时间戳，判断是否过期
		timeStamp = obj.getIPInfoConfig("user", "time_stamp");
		expire = float(_GG("ClientConfig").Config().Get("local", "user_info_expire", 60 * 60 * 24 * 10)); # 服务配置
		if not timeStamp or float(time.time()) - float(timeStamp) > expire:
			obj.removeIPInfoConfig("user"); # 移除配置
			return;
		# 读取配置
		userName, password = obj.getIPInfoConfig("user", "name"), obj.getIPInfoConfig("user", "password");
		if userName and password:
			# 登录回调
			def onLogin(respData):
				if respData and respData.isSuccess:
					_GG("EventDispatcher").dispatch(_GG("EVENT_ID").LOGIN_SUCCESS_EVENT, respData.userInfo);
				pass;
			# 请求服务
			_GG("CommonClient").callService("Login", "LoginReq", {
				"name" : userName,
				"password" : password,
			}, asynCallback = onLogin);

	# 更新update脚本
	def checkAndUpdateScript(self, dirPath):
		assetsPath = os.path.join(dirPath, "assets");
		if not os.path.exists(assetsPath):
			return;
		def getUpdateFile(dPath):
			for fileName in os.listdir(dPath):
				filePath = os.path.join(dPath, fileName);
				if os.path.isfile(filePath) and re.search(r"^update\.py.*$", fileName):
					return filePath;
		# 获取更新文件名
		filePath, updateFile = getUpdateFile(assetsPath), getUpdateFile(_GG("g_AssetsPath"));
		if filePath:
			if updateFile:
				os.remove(updateFile);
			updateFile = os.path.join(_GG("g_AssetsPath"), fileName);
			shutil.copyfile(filePath, updateFile);
		return updateFile;

