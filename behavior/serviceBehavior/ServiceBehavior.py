# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-06 23:14:13
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-11 23:22:24
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
			"basePath" : _GG("g_CommonPath") + "behavior\\",
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
		# todo 获取保存到本地的账号密码
		if not os.path.exists(_GG("g_ProjectPath")+"date/ip_info.ini"):
			return;
		# 读取配置
		conf = ConfigParser.RawConfigParser();
		conf.read(_GG("g_ProjectPath")+"date/ip_info.ini");
		if not (conf.has_option("user", "name") and conf.has_option("user", "password")):
			return;
		userName, password = conf.get("user", "name"), conf.get("user", "password");
		# 登录回调
		def onLogin(retData):
			if not retData or retData.isSuccess:
				return;
			# 登录成功后的处理
			data = _GG("CommonClient").decodeBytes(retData.data);
			# todo 通知更新用户信息[retData]
			pass;
		# 请求服务
		_GG("CommonClient").callService("Login", "LoginReq", {
			"name" : userName,
			"password" : password,
		}, asynCallback = onLogin);
