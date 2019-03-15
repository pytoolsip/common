# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-06 23:14:13
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-15 18:29:27
import os;

from _Global import _GG;
from function.base import *;

def getExposeData():
	return {
		# "exposeDataName" : {},
	};

def getExposeMethod(DoType):
	return {
		"checkUpdateCommon" : DoType.AddToRear,
		"autoLoginIP" : DoType.AddToRear,
	};

class ServiceBehavior(_GG("BaseBehavior")):
	def __init__(self, depends = []):
		self.appendDepends(depends);
		super(ServiceBehavior, self).__init__(depends);
		self.className_ = ServiceBehavior.__name__;
		pass;

	def getExposeData(self):
		return getExposeData(); # 获取暴露出的数据

	def getExposeMethod(self, DoType):
		return getExposeMethod(DoType); # 获取暴露出的方法接口

	def appendDepends(self, depends = []):
		depends.append({
			"path" : "serviceBehavior/UpDownloadBehavior",
			"basePath" : _GG("g_CommonPath") + "behavior/",
		});
		depends.append({
			"path" : "serviceBehavior/IPInfoBehavior",
			"basePath" : _GG("g_CommonPath") + "behavior/",
		});

	# 检测更新Common
	def checkUpdateCommon(self, obj, _retTuple = None):
		resp = _GG("CommonClient").callService("Update", "UpdateReq", {"name" : "common", "version" : _GG("AppConfig")["version"]});
		if resp and not resp.isUpToDate:
			msgDialog = wx.MessageDialog(obj, "检测有更新版本，是否确认更新？", "检测common版本！", style = wx.YES_NO|wx.ICON_QUESTION);
			if msgDialog.ShowModal() == wx.ID_YES:
				info = resp.updateInfo;
				fileNme = info.url.split("/")[-1];
				obj.download(info.url, _GG("g_ProjectPath")+"date/update/"+fileNme, info.totalSize);

	# 自动登录平台
	def autoLoginIP(self, obj, _retTuple = None):
		# 根据时间戳，判断是否过期
		timeStamp = obj.getIPInfoConfig("user", "time_stamp");
		expire = float(_GG("ClientConfig").Config().Get("local", "user_info_expire", 60 * 60 * 24 * 10)); # 服务配置
		if not timeStamp or time.time() - float(timeStamp) > expire:
			obj.removeIPInfoConfig("user"); # 移除配置
			return;
		# 读取配置
		userName, password = obj.getIPInfoConfig("user", "name"), obj.getIPInfoConfig("user", "password");
		if userName and password:
			# 登录回调
			def onLogin(respData):
				if respData and respData.isSuccess:
					_GG("EventDispatcher").dispatch(_GG("EVENT_ID").LOGIN_SUCCESS_EVENT, respData);
				pass;
			# 请求服务
			_GG("CommonClient").callService("Login", "LoginReq", {
				"name" : userName,
				"password" : password,
			}, asynCallback = onLogin);
