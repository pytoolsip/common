# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-07 20:34:34
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-23 22:14:20
import wx;
import urllib;
import paramiko;
import zipfile;
import threading;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"download" : DoType.AddToRear,
		"upload" : DoType.AddToRear,
		"zipFile" : DoType.AddToRear,
		"unzipFile" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class UpDownloadBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(UpDownloadBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = UpDownloadBehavior.__name__;
		pass;

	# 下载文件
	def download(self, obj, url, filePath, totalSize, _retTuple = None):
		dialogCtr = _GG("WindowObject").CreateDialogCtr(_GG("g_CommonPath") + "dialog/DownloadDialog", params = {"title" : "文件下载", "size" : (200,-1)});
		def schedule(block, size, totalSize):
			dialogCtr.updateDialog({"size" : block*size});
		urllib.urlretrieve(url, filePath, schedule);
		dialogCtr.getUI().start(totalSize = totalSize);

	# 上传文件
	def upload(self, obj, filePath, data, callback = None, _retTuple = None):
		def uploadFile(filePath, data, callback = None):
			transport = paramiko.Transport((data["host"], int(data["port"])));
			transport.banner_timeout = 300
			transport.connect(username = data["user"], password = data["password"]);
			sftp = paramiko.SFTPClient.from_transport(transport);
			sftp.put(filePath, data["url"]);
			transport.close();
			if callable(callback):
				wx.CallAfter(callback);
		threading.Thread(target = uploadFile, args = (filePath, data, callback)).start();

	# 压缩文件
	def zipFile(self, obj, dirpath, filePath, finishCallback = None, _retTuple = None):
		totalSize = self.getDirPathSize(dirpath);
		def zipMethod(dirpath, filePath, totalSize, callback, lastCallback):
			zf = zipfile.ZipFile(filePath,'w', zipfile.ZIP_DEFLATED);
			completeSize = 0;
			for root, _, files in os.walk(dirpath):
				# 去掉目标根路径，只对目标文件夹下边的文件进行压缩
				for file in files:
					if os.path.splitext(file)[-1] not in [".pyc"]: # 过滤文件
						zf.write(os.path.join(root, file), os.path.join(root.replace(dirpath, ''), file));
						completeSize += os.path.getsize(os.path.join(root, file));
				callback(completeSize/totalSize, root); # 回调函数
			zf.close();
			if callable(lastCallback):
				wx.CallAfter(lastCallback); # 完成后的回调
		proDialog = wx.ProgressDialog("压缩工具包", "", style = wx.PD_APP_MODAL|wx.PD_CAN_SKIP|wx.PD_ELAPSED_TIME|wx.PD_ESTIMATED_TIME|wx.PD_REMAINING_TIME);
		def updateProDialog(value, path):
			value = proDialog.GetRange() * value;
			if value >= proDialog.GetRange():
				wx.CallAfter(proDialog.Update, proDialog.GetRange(), "已完成压缩，包路径为：\n" + str(filePath));
			else:
				wx.CallAfter(proDialog.Update, value, "正在压缩\n" + str(path));
		threading.Thread(target = zipMethod, args = (dirpath, filePath, totalSize, updateProDialog, finishCallback)).start();
		proDialog.Update(0, "开始压缩\n" + str(filePath));
		proDialog.ShowModal();

	# 解压文件
	def unzipFile(self, obj, filePath, dirpath, _retTuple = None):
		zf = zipfile.ZipFile(filePath, "r");
		for file in zf.namelist():
			zf.extract(file, dirpath);

	# 获取文件夹大小
	def getDirPathSize(self, dirpath):
		totalSize = 0;
		for root, _, files in os.walk(dirpath):
			totalSize += sum([os.path.getsize(os.path.join(root, file)) for file in files]);
		return totalSize;