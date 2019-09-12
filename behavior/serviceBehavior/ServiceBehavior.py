# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-06 23:14:13
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-27 18:38:07
import os,re;

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

	# 请求更新平台信息
	def reqUpdateIP(self, obj, _retTuple = None):
		resp = _GG("CommonClient").callService("UpdateIP", "UpdateIPReq", {"version" : _GG("AppConfig")["version"]});
		if resp and resp.code == 0:
			return True, resp.reqUrl;
		return False, "";

	def checkUpdateIP(self, obj, _retTuple = None):
		ret, reqUrl = self.reqUpdateIP(obj);
		if ret:
			if _GG("WindowObject").CreateMessageDialog("检测有更新版本，是否确认更新？", "检测平台版本", style = wx.OK|wx.ICON_QUESTION) == wx.ID_OK:
				updateFile = self.getUpdateFile();
				if not updateFile:
					return False;
				_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_APP_EVENT, {"reqUrl" : reqUrl, "updateFile" : updateFile});
			else:
				return False;
		return True;

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

	# 获取更新文件
	def getUpdateFile(self):
		updatePath = os.path.join(updateFile, "update");
		if not os.path.exists(updatePath):
			return "";
		# 获取更新脚本文件
		for fileName in os.listdir(updatePath):
			filePath = os.path.join(updatePath, fileName);
			if os.path.isfile(filePath) and re.search(r"^update\.py.*$", fileName):
				return filePath;
		return "";
