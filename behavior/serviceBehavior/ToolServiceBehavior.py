# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-20 19:39:49
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-20 23:27:42

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"_uploadTool_" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		{
			"path" : "serviceBehavior/UpDownloadBehavior", 
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
	];

class ToolServiceBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(ToolServiceBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = ToolServiceBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	def _uploadTool_(self, obj, _retTuple = None):
		def onBlurName(name, callback):
			# 请求服务的回调
			def checkName(respData):
				if not respData:
					callback("网络请求失败！", False);
				elif respData.isSuccess:
					callback("该分类路径下已存在相同工具名！", False);
				else:
					callback("");
			# 请求服务
			_GG("CommonClient").callService("Request", "Req", {
				"key" : "VertifyToolName",
				"data" : _GG("CommonClient").encodeBytes({"name" : name}),
			}, asynCallback = checkName);
		def onUpload(uploadInfo):
			respData = _GG("CommonClient").callService("Upload", "UploadReq", uploadInfo);
			# if respData and respData.isPermit:
			# 	respData = _GG("CommonClient").callService("Upload", "UploadReq", uploadInfo);
			# 	_GG("WindowObject").CreateMessageDialog("登录成功，是否保存账户密码到本地？", "登录账号", callback = setIPInfoConfig, style = wx.OK|wx.CANCEL|wx.ICON_QUESTION)
			# else:
			# 	_GG("WindowObject").CreateMessageDialog("登录失败，请重新登录！", "登录账号", style = wx.OK|wx.ICON_INFORMATION);
			return respData and respData.isSuccess or False;
		# 显示弹窗
		_GG("WindowObject").CreateDialogCtr(_GG("g_CommonPath") + "dialog/UploadDialog", params = {
			"name" : {
				"onBlur" : onBlurName,
			},
			"category" : {
				"choicesInfo" : {
					"cols" : 2,
					"firstChoices" : [u"开发工具", u"产品工具", u"娱乐工具"],
					"choiceDict" : {
						u"开发工具" : [u"文件处理", u"数据处理"],
						u"产品工具" : [u"文件处理", u"数据处理"],
						u"娱乐工具" : [u"小游戏"],
					},
				},
			},
			"onOk" : onUpload,
		});
