# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-16 11:25:09
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2020-02-05 19:53:05
import wx;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"_loginIP_" : DoType.AddToRear,
		"_logoutIP_" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		{
			"path" : "serviceBehavior/IPInfoBehavior", 
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
	];

class UserServiceBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(UserServiceBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = UserServiceBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	def _loginIP_(self, obj, _retTuple = None):
		def onLogin(loginInfo):
			respData = _GG("CommonClient").callService("Login", "LoginReq", {
				"name" : loginInfo["name"],
				"pwd" : obj.encodeStrByPublicKey(loginInfo["password"]),
			});
			if respData and respData.code == 0:
				_GG("EventDispatcher").dispatch(_GG("EVENT_ID").LOGIN_SUCCESS_EVENT, {"userInfo" : respData.userInfo, "expire" : respData.expire});
				# 保存用户信息
				obj.setIPInfoConfig("user", "name", respData.userInfo.name);
				obj.setIPInfoConfig("user", "pwd", respData.userInfo.pwd);
				obj.setIPInfoConfig("user", "email", respData.userInfo.email);
				obj.setIPInfoConfig("user", "expire", respData.expire);
				obj.setIPInfoConfig("user", "time_stamp", time.time());
			else:
				_GG("WindowObject").CreateMessageDialog("登录失败，请重新登录！", "登录平台", style = wx.OK|wx.ICON_INFORMATION);
			return respData and respData.code == 0 or False;
		def onReqLogin(loginInfo):
			# 请求公钥数据
			respData = _GG("CommonClient").callService("Request", "Req", {
				"key" : "ReqPublicKey",
				"data" : _GG("CommonClient").encodeBytes({}),
			});
			if respData and respData.code == 0:
				msgData = _GG("CommonClient").decodeBytes(respData.data);
				obj.setEncodePublicKey(msgData["key"]); # 保存公钥数据
			onLogin(loginInfo); # 登陆平台
		# 显示弹窗
		_GG("WindowObject").CreateDialogCtr(_GG("g_CommonPath") + "dialog/LoginDialog", params = {
			"onOk" : onReqLogin,
		});

	def _logoutIP_(self, obj, _retTuple = None):
		_GG("EventDispatcher").dispatch(_GG("EVENT_ID").LOGOUT_SUCCESS_EVENT, {
			"userName" : obj.getIPInfoConfig("user", "name"),
		});
		obj.removeIPInfoConfig("user"); # 移除配置