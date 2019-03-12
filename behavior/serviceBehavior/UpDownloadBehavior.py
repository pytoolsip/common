# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-07 20:34:34
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-09 14:44:57
import urllib;
import paramiko;
import zipfile;

from _Global import _GG;
from function.base import *;

def getExposeData():
	return {
		# "exposeDataName" : {},
	};

def getExposeMethod(DoType):
	return {
		"download" : DoType.AddToRear,
		"upload" : DoType.AddToRear,
		"zipFile" : DoType.AddToRear,
		"unzipFile" : DoType.AddToRear,
	};

class UpDownloadBehavior(_GG("BaseBehavior")):
	def __init__(self, depends = []):
		super(UpDownloadBehavior, self).__init__(depends);
		self.className_ = UpDownloadBehavior.__name__;
		pass;

	def getExposeData(self):
		return getExposeData(); # 获取暴露出的数据

	def getExposeMethod(self, DoType):
		return getExposeMethod(DoType); # 获取暴露出的方法接口

	# 下载文件
	def download(self, obj, url, filePath, totalSize, _retTuple = None):
		dialog = CreateCtr(_GG("g_CommonPath") + "dialog\\DownloadDialog", obj, params = {"title" : "文件下载", "size" : (200,-1)});
		def schedule(block, size, totalSize):
			dialog.updateDialog({"size" : block*size});
		urllib.urlretrieve(url, filePath, schedule);
		dialog.start(totalSize = totalSize);

	# 上传文件
	def upload(self, obj, filePath, url, data, _retTuple = None):
		transport = paramiko.Transport((data["host"], data["port"]));
		transport.connect(username = data["name"], password = data["password"]);
		sftp = paramiko.SFTPClient.from_transport(transport);
		sftp.put(filePath, url);
		transport.close();

	# 压缩文件
	def zipFile(self, obj, dirpath, filePath, _retTuple = None):
		zf = zipfile.ZipFile(filePath,'w', zipfile.ZIP_DEFLATED);
		for path, _, filenames in os.walk(dirpath):
			# 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
			fpath = path.replace(dirpath,'');
			for filename in filenames:
				zf.write(os.path.join(path, filename), os.path.join(fpath, filename));
		zf.close();

	# 解压文件
	def unzipFile(self, obj, filePath, dirpath, _retTuple = None):
		zf = zipfile.ZipFile(filePath, "r");
		for file in zf.namelist():
			zf.extract(file, dirpath);