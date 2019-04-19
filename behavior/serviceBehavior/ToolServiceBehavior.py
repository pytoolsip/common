# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-20 19:39:49
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 00:33:26
import wx;
import hashlib;
import os, shutil;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"_uploadTool_" : DoType.AddToRear,
		"_showToolInfo_" : DoType.AddToRear,
		"_downloadTool_" : DoType.AddToRear,
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
		if _GG("CommonClient").getUserId() < 0:
			_GG("WindowObject").CreateMessageDialog("请先登录账号！", "上传工具", style = wx.OK|wx.ICON_INFORMATION);
			return;
		def onBlurName(name, callback):
			# 请求服务的回调
			def checkName(respData):
				if not respData:
					callback("网络请求失败！", False);
				elif respData.isSuccess:
					data = _GG("CommonClient").decodeBytes(respData.data);
					if "version" in data:
						callback("", onlineVersion = data["version"]);
					else:
						callback("");
				else:
					callback("该分类路径下已存在相同工具名！", False);
			# 请求服务
			_GG("CommonClient").callService("Request", "Req", {
				"key" : "VertifyToolName",
				"data" : _GG("CommonClient").encodeBytes({"name" : name}),
			}, asynCallback = checkName);
		def onUpload(uploadInfo):
			respData = _GG("CommonClient").callService("Upload", "UploadReq", {
				"uid" : _GG("CommonClient").getUserId(),
				"category" : uploadInfo["category"],
				"name" : uploadInfo["name"],
				"version" : uploadInfo["version"],
				"commonVersion" : uploadInfo["commonVersion"],
				"description" : uploadInfo["description"],
			});
			if not respData:
				_GG("WindowObject").CreateMessageDialog("网络请求失败！", "上传工具", style = wx.OK|wx.ICON_ERROR);
			elif not respData.isPermit:
				_GG("WindowObject").CreateMessageDialog("上传失败，请检测上传信息！", "上传工具", style = wx.OK|wx.ICON_ERROR);
			else:
				msgDlg = _GG("WindowObject").CreateMessageDialog("正在上传工具【%s】..."%uploadInfo["name"], "上传工具", isShow = False, style = wx.OK|wx.ICON_INFORMATION)
				token = _GG("CommonClient").decodeBytes(respData.token);
				def callback():
					def asynCallback(respData):
						msgDlg.Destroy();
						if not respData:
							_GG("WindowObject").CreateMessageDialog("网络连接失败！", "上传工具", style = wx.OK|wx.ICON_ERROR)
						elif respData.isSuccess:
							_GG("WindowObject").CreateMessageDialog("上传工具【%s】成功。"%uploadInfo["name"], "上传工具", style = wx.OK|wx.ICON_INFORMATION);
						else:
							_GG("WindowObject").CreateMessageDialog("保存工具【%s】包数据失败！"%uploadInfo["name"], "上传工具", style = wx.OK|wx.ICON_ERROR)
					_GG("CommonClient").callService("Uploaded", "UploadReq", {
						"uid" : _GG("CommonClient").getUserId(),
						"category" : uploadInfo["category"],
						"name" : uploadInfo["name"],
						"version" : uploadInfo["version"],
						"commonVersion" : uploadInfo["commonVersion"],
						"description" : uploadInfo["description"],
					}, asynCallback = asynCallback);
				try:
					obj.upload(uploadInfo["filePath"], token, callback = callback);
					msgDlg.ShowModal();
				except Exception as e:
					msgDlg.Destroy();
					_GG("WindowObject").CreateMessageDialog("上传失败！%s"%e, "上传工具", style = wx.OK|wx.ICON_ERROR)
			return respData and respData.isPermit or False;
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

	def _showToolInfo_(self, obj, data, _retTuple = None):
		def onDownload():
			if "key" not in data:
				return;
			tkey = data.get("key", "");
			def onResp(respData):
				if not respData:
					_GG("WindowObject").CreateMessageDialog("网络请求失败！", "下载工具", style = wx.OK|wx.ICON_ERROR);
				elif not respData.isExist:
					_GG("WindowObject").CreateMessageDialog("所要下载的工具不存在！", "下载工具", style = wx.OK|wx.ICON_ERROR);
				else:
					toolsPath = _GG("g_DataPath")+"tools/";
					fileName = os.path.basename(respData.url);
					def onComplete(filePath):
						# 重置文件夹
						dirpath = toolsPath + tkey;
						if os.path.exists(dirpath):
							shutil.rmtree(dirpath);
						os.mkdir(dirpath);
						# 解压文件
						def afterUnzip():
							# 删除压缩文件
							os.remove(filePath);
							# 更新左侧工具树
							_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_WINDOW_LEFT_VIEW, {
								"action" : "add",
								"key" : tkey,
								"trunk" : "data/tools",
								"branch" : tkey,
								"path" : "MainView",
								"name" : respData.toolInfo.name,
								"category" : respData.toolInfo.category,
								"description" : respData.toolInfo.description,
								"version" : respData.toolInfo.version,
								"author" : respData.toolInfo.author,
							});
						obj.unzipFile(filePath, dirpath, finishCallback = afterUnzip);
						pass;
					# 下载文件
					obj.download(respData.url, toolsPath+fileName, respData.totalSize, onComplete = onComplete);
				pass;
			_GG("CommonClient").callService("Download", "DownloadReq", {
				"key" : tkey,
				"commonVersion" : _GG("AppConfig")["version"],
			}, asynCallback = onResp);
			pass;
		_GG("WindowObject").CreateDialogCtr(_GG("g_CommonPath") + "dialog/ToolInfoDialog", params = {
			"name" : data.get("name", ""),
			"path" : data.get("path", ""),
			"version" : data.get("version", ""),
			"author" : data.get("author", ""),
			"description" : data.get("description", {}),
			"download" : data.get("download", {
				"onDownload" : onDownload,
			}),
		});

	def _downloadTool_(self, obj, _retTuple = None):
		teDialog = _GG("WindowObject").CreateWxDialog("TextEntryDialog", "请输入工具ID：", "下载工具");
		if teDialog.ShowModal() == wx.ID_OK:
			tkey = teDialog.GetValue();
			def onRequestToolInfo(respData):
				if not respData:
					_GG("WindowObject").CreateMessageDialog("网络请求失败！", "下载工具", style = wx.OK|wx.ICON_ERROR);
				elif respData.isSuccess:
					data = _GG("CommonClient").decodeBytes(respData.data);
					obj._showToolInfo_({
						"key" : tkey,
						"name" : data.get("title", ""),
						"path" : data.get("category", ""),
						"version" : data.get("version", ""),
						"author" : data.get("author", ""),
						"description" : {
							"value" : data.get("description", ""),
						},
					});
				else:
					if _GG("WindowObject").CreateMessageDialog("输入的工具ID不存在！\n请重新输入!", "下载工具", style = wx.OK|wx.ICON_ERROR) == wx.ID_OK:
						wx.CallAfter(obj._downloadTool_);
			# 请求服务
			_GG("CommonClient").callService("Request", "Req", {
				"key" : "RequestToolInfo",
				"data" : _GG("CommonClient").encodeBytes({"key" : tkey, "commonVersion" : _GG("AppConfig")["version"]}),
			}, asynCallback = onRequestToolInfo);