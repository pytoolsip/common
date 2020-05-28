# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-20 19:39:49
# @Last Modified by:   JinZhang
# @Last Modified time: 2020-05-21 17:22:39
import wx;
import hashlib;
import os, shutil;
import threading;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"_showToolInfo_" : DoType.AddToRear,
		"_downloadTool_" : DoType.AddToRear,
		"_dealDepends_" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		{
			"path" : "serviceBehavior/UpDownloadBehavior", 
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
		{
			"path" : "verifyBehavior/VerifyDependsBehavior",
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

	def _showToolInfo_(self, obj, data, _retTuple = None):
		if "key" not in data:
			return;
		tkey = data.get("key", "");
		def onDownload(isUpdate = False):
			def onResp(respData):
				if not respData:
					_GG("WindowObject").CreateMessageDialog("网络请求失败！", "下载工具", style = wx.OK|wx.ICON_ERROR);
				elif respData.code != 0:
					_GG("Log").d("Download resp ->", respData);
					_GG("WindowObject").CreateMessageDialog("所要下载的工具不存在！", "下载工具", style = wx.OK|wx.ICON_ERROR);
				else:
					toolsPath = _GG("g_DataPath")+"tools/";
					fileName = os.path.basename(respData.url);
					def onComplete(filePath):
						# 重置文件夹【会移除原有文件夹】
						dirpath = toolsPath + tkey + "_temp";
						if os.path.exists(dirpath):
							shutil.rmtree(dirpath);
						os.makedirs(dirpath);
						# 解压文件
						def afterUnzip():
							# 删除压缩文件
							os.remove(filePath);
							# 处理依赖模块
							tgtDirPath = toolsPath + tkey;
							def afterDealDepends():
								if os.path.exists(tgtDirPath):
									shutil.rmtree(tgtDirPath);
								shutil.move(dirpath, tgtDirPath);
								# 更新左侧工具树
								_GG("EventDispatcher").dispatch(_GG("EVENT_ID").UPDATE_WINDOW_LEFT_VIEW, {
									"action" : "add",
									"key" : tkey,
									"trunk" : "g_DataPath",
									"branch" : "/".join(["tools", tkey, "tool"]),
									"path" : "MainView",
									"name" : respData.toolInfo.name,
									"category" : respData.toolInfo.category,
									"description" : respData.toolInfo.description,
									"version" : respData.toolInfo.version,
									"author" : respData.toolInfo.author,
								});
							def failDealDepends():
								_GG("WindowObject").CreateMessageDialog("工具安装失败！工具所依赖的模块版本不匹配！", "安装工具", style = wx.OK|wx.ICON_ERROR);
							obj._dealDepends_(tgtDirPath, dirpath, finishCallback = afterDealDepends, failedCallback = failDealDepends);
						obj.unzipFile(filePath, dirpath, finishCallback = afterUnzip);
						# 记录下载数据
						_GG("CommonClient").callService("DownloadRecord", "DownloadRecordReq", {
							"key" : tkey,
							"downloadKey" : respData.downloadKey,
						});
						pass;
					# 下载文件
					obj.download(respData.url, toolsPath+fileName, respData.totalSize, onComplete = onComplete);
				pass;
			_GG("CommonClient").callService("Download", "DownloadReq", {
				"key" : tkey,
				"IPBaseVer" : GetBaseVersion(_GG("ClientConfig").UrlConfig().GetIPVersion()),
			}, asynCallback = onResp);
			pass;
		def checkDownload(callback = None):
			def onRequestToolInfo(respData):
				if not respData:
					_GG("WindowObject").CreateMessageDialog("网络请求失败！", "下载工具", style = wx.OK|wx.ICON_ERROR);
				elif respData.code == 0:
					itemData = _GG("WindowObject").MainWindowCtr.getItemDataByKey(tkey);
					if itemData:
						if CheckVersion(respData.toolInfo.version, itemData.get("version", "")) and callable(callback):
							callback(True);
					elif callable(callback):
						callback();
				pass;
			_GG("CommonClient").callService("ReqToolInfo", "ToolReq", {
				"key" : tkey,
				"IPBaseVer" : GetBaseVersion(_GG("ClientConfig").UrlConfig().GetIPVersion()),
			}, asynCallback = onRequestToolInfo);
			pass;
		_GG("WindowObject").CreateDialogCtr(_GG("g_CommonPath") + "dialog/ToolInfoDialog", params = {
			"name" : data.get("name", ""),
			"path" : data.get("path", ""),
			"version" : data.get("version", ""),
			"author" : data.get("author", ""),
			"description" : data.get("description", {}),
			"download" : data.get("download", {
				"onDownload" : onDownload,
				"checkDownload" : checkDownload,
			}),
		}, isRecreate = True);

	def _downloadTool_(self, obj, _retTuple = None):
		teDialog = _GG("WindowObject").CreateWxDialog("TextEntryDialog", "请输入工具ID：", "下载工具");
		if teDialog.ShowModal() == wx.ID_OK:
			tkey = teDialog.GetValue();
			if not tkey:
				_GG("WindowObject").CreateMessageDialog("输入的工具ID不能为空！\n请重新输入!", "下载工具", style = wx.OK|wx.ICON_ERROR);
				wx.CallAfter(obj._downloadTool_);
				return;
			def onRequestToolInfo(respData):
				if not respData:
					_GG("WindowObject").CreateMessageDialog("网络请求失败！", "下载工具", style = wx.OK|wx.ICON_ERROR);
				elif respData.code == 0 and respData.toolInfo:
					toolInfo = respData.toolInfo;
					obj._showToolInfo_({
						"key" : tkey,
						"name" : toolInfo.name,
						"path" : toolInfo.category,
						"version" : toolInfo.version,
						"author" : toolInfo.author,
						"description" : {
							"value" : toolInfo.description,
						},
					});
				else:
					_GG("WindowObject").CreateMessageDialog("输入的工具ID不存在！\n请重新输入!", "下载工具", style = wx.OK|wx.ICON_ERROR);
					wx.CallAfter(obj._downloadTool_);
			# 请求服务
			_GG("CommonClient").callService("ReqToolInfo", "ToolReq", {
				"key" : tkey,
				"IPBaseVer" : GetBaseVersion(_GG("ClientConfig").UrlConfig().GetIPVersion()),
			}, asynCallback = onRequestToolInfo);

	# 处理依赖模块
	def _dealDepends_(self, obj, srcPath, targetPath, finishCallback = None, failedCallback = None, _retTuple = None):
		dependMapFile = _GG("g_DataPath") + "depend_map.json";
		proDialog = wx.ProgressDialog("处理依赖模块", "", style = wx.PD_APP_MODAL|wx.PD_ELAPSED_TIME|wx.PD_ESTIMATED_TIME|wx.PD_REMAINING_TIME|wx.PD_AUTO_HIDE);
		def onInstall(modvalue, value, isEnd = False):
			if not isEnd:
				wx.CallAfter(proDialog.Update, value, f"正在安装模块【{mode}】...");
			else:
				wx.CallAfter(proDialog.Update, value, f"成功安装模块【{mode}】。");
			pass;
		def onUninstall(modvalue, value, isEnd = False):
			if not isEnd:
				wx.CallAfter(proDialog.Update, value, f"正在卸载模块【{mode}】...");
			else:
				wx.CallAfter(proDialog.Update, value, f"成功卸载模块【{mode}】。");
			pass;
		def onFinish(isChange, dependMap, isSuccess = True):
			if not isSuccess:
				wx.CallAfter(proDialog.Update, 0, f"依赖模块处理失败！");
				if callable(failedCallback):
					wx.CallAfter(failedCallback);
				return;
			wx.CallAfter(proDialog.Update, 1, f"完成依赖模块的处理。");
			if isChange:
				wx.CallAfter(obj._updateDependMap_, dependMap, dependMapFile);
			if callable(finishCallback):
				wx.CallAfter(finishCallback);
		threading.Thread(target = obj._checkDependMap_, args = (srcPath, targetPath, dependMapFile, _GG("g_PythonPath"), onInstall, onUninstall, onFinish)).start();
		proDialog.Update(0, "开始处理依赖模块...");
		proDialog.ShowModal();