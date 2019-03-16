# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-16 11:25:09
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:48:37

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"_loginIP_" : DoType.AddToRear,
		"_registerIP_" : DoType.AddToRear,
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
		super(UserServiceBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__);
		self._className_ = UserServiceBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	def _loginIP_(self, obj, _retTuple = None):
		def onBlurName(name, callback):
			# 请求服务的回调
			def checkName(respData):
				if not respData:
					callback("网络请求失败！", False);
				elif not respData.isSuccess:
					callback("该用户名不存在！", False);
				else:
					callback("");
			# 请求服务
			_GG("CommonClient").callService("Request", "Req", {
				"key" : "VertifyUserName",
				"data" : _GG("CommonClient").encodeBytes({"name" : name}),
			}, asynCallback = checkName);
		def onLogin(loginInfo):
			respData = _GG("CommonClient").callService("Login", "LoginReq", loginInfo);
			if respData and respData.isSuccess:
				_GG("EventDispatcher").dispatch(_GG("EVENT_ID").LOGIN_SUCCESS_EVENT, respData.userInfo);
				if _GG("WindowObject").ShowMessageDialog("登录成功，是否保存账户密码到本地？", "登录账号", style = wx.OK|wx.CANCEL|wx.ICON_QUESTION) == wx.ID_OK:
					obj.setIPInfoConfig("user", "name", loginInfo["name"]);
					obj.setIPInfoConfig("user", "password", loginInfo["password"]);
					obj.setIPInfoConfig("user", "time_stamp", time.time());
			else:
				_GG("WindowObject").ShowMessageDialog("登录失败，请重新登录！", "登录账号", style = wx.OK|wx.ICON_INFORMATION);
			return respData and respData.isSuccess or False;
		# 显示弹窗
		_GG("WindowObject").CreateDialogCtr(_GG("g_CommonPath") + "dialog/LoginDialog", params = {
			# "name" : {
			# 	"onBlur" : onBlurName,
			# },
			"onOk" : onLogin,
		});

	def _registerIP_(self, obj, _retTuple = None):
		def onBlurName(name, callback):
			# 请求服务的回调
			def checkName(respData):
				if not respData:
					callback("网络请求失败！", False);
				elif respData.isSuccess:
					callback("该用户名已存在！", False);
				else:
					callback("用户名校验通过！");
			# 请求服务
			_GG("CommonClient").callService("Request", "Req", {
				"key" : "VertifyUserName",
				"data" : _GG("CommonClient").encodeBytes({"name" : name}),
			}, asynCallback = checkName);
		def onBlurEmail(email, callback):
			# 请求服务的回调
			def checkEmail(respData):
				if not respData:
					callback("网络请求失败！", False);
				elif respData.isSuccess:
					callback("该邮箱已被使用！", False);
				else:
					callback("邮箱校验通过！");
			# 请求服务
			_GG("CommonClient").callService("Request", "Req", {
				"key" : "VertifyUserEmail",
				"data" : _GG("CommonClient").encodeBytes({"email" : email}),
			}, asynCallback = checkEmail);
		def onBlurVeriCode(email, code, callback):
			# 请求服务的回调
			def checkCode(respData):
				if not respData:
					callback("网络请求失败！", False);
				elif not respData.isSuccess:
					callback("验证码输入错误！", False);
				else:
					callback("验证码校验通过！");
			# 请求服务
			_GG("CommonClient").callService("Request", "Req", {
				"key" : "VertifyVerificationCode",
				"data" : _GG("CommonClient").encodeBytes({"email" : email, "code" : code}),
			}, asynCallback = checkCode);
		def onSendVeriCode(email, callback):
			# 请求服务的回调
			def checkResp(respData):
				if respData and respData.isSuccess:
					callback(respData.data["expire"]);
				else:
					_GG("WindowObject").ShowMessageDialog("发送失败，请检测邮箱是否正确！", "发送校验码", style = wx.OK|wx.ICON_ERROR);
			# 请求服务
			_GG("CommonClient").callService("Request", "Req", {
				"key" : "SendVerificationCode",
				"data" : _GG("CommonClient").encodeBytes({"email" : email}),
			}, asynCallback = checkResp);
		def onRegister(registerInfo):
			respData = _GG("CommonClient").callService("Register", "RegisterReq", registerInfo);
			if respData and respData.isSuccess:
				_GG("WindowObject").ShowMessageDialog("注册成功。", "注册账号", style = wx.OK|wx.ICON_INFORMATION);
			else:
				if respData and respData.data:
					data = _GG("CommonClient").decodeBytes(respData.data);
					if "content" in data:
						_GG("WindowObject").ShowMessageDialog(data["content"], "注册账号", style = wx.OK|wx.ICON_INFORMATION);
						return False;
				_GG("WindowObject").ShowMessageDialog("注册失败，请重新注册！", "注册账号", style = wx.OK|wx.ICON_INFORMATION);
			return respData and respData.isSuccess or False;
		# 显示弹窗
		_GG("WindowObject").CreateDialogCtr(_GG("g_CommonPath") + "dialog/RegisterDialog", params = {
			"name" : {
				"onBlur" : onBlurName,
			},
			"email" : {
				"onBlur" : onBlurEmail,
			},
			"veriCode" : {
				"onBlur" : onBlurVeriCode,
				"onBtn" : onSendVeriCode,
			},
			"onOk" : onRegister,
		});