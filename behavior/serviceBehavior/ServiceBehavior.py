# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-06 23:14:13
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-27 18:38:07
import os;

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
		resp = _GG("CommonClient").callService("Update", "UpdateIPReq", {"uid" : _GG("CommonClient").getUserId(), "version" : _GG("AppConfig")["version"]});
		if resp and not resp.isUpToDate:
			msgDialog = wx.MessageDialog(obj, "检测有更新版本，是否确认更新？", "检测平台版本！", style = wx.YES_NO|wx.ICON_QUESTION);
			if msgDialog.ShowModal() == wx.ID_YES:
				dirPath = _GG("g_DataPath")+"update/pytoolsip/";
				if not os.path.exists(dirPath):
					os.mkdir(dirPath);
				fileNme = resp.url.split("/")[-1];
				obj.download(resp.url, dirPath+fileNme, resp.totalSize);

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
