# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-11-21 20:06:13
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-12-01 11:55:22

import os;
import re;
import json;

def checkFilePath(filePath):
	if re.search("\w+\.py$", filePath):
		return True;
	return False;

# 获取所有文件列表
def getFileList(path):
	fileList = [];
	fileNameMap = {};
	def checkAllFile(dirPath):
		for file in os.listdir(dirPath):
			isCanImport = False;
			filePath = os.path.join(dirPath, file);
			if os.path.isdir(filePath):
				checkAllFile(filePath);
				isCanImport = True;
			elif checkFilePath(filePath):
				fileList.append(filePath);
				isCanImport = True;
			if isCanImport:
				# 获取文件名
				result = re.match("(\w+)(\.py)?$", file);
				if result:
					fileNameMap[result.group(1)] = 1;
	if os.path.isdir(path):
		checkAllFile(path);
	return fileList, fileNameMap;

# 获取所有文件列表中import的模块名
def getImportMapByFileList(fileList, excludeMaps = []):
	importMap = {};
	def checkImportMap(file):
		with open(file, "rb") as f:
			for line in f.readlines():
				line = line.decode("utf-8", "ignore");
				result = re.match("^from (\w+)\.?.*import.*", line);
				if result and not checkKeyInExcludeMaps(result.group(1), excludeMaps):
					importMap[result.group(1)] = 1;
				else:
					result = re.match("^import (\w+)\.?.*", line);
					if result and not checkKeyInExcludeMaps(result.group(1), excludeMaps):
						importMap[result.group(1)] = 1;
			f.close();
	for filePath in fileList:
		checkImportMap(filePath);
	return importMap;

# 检测key值是否在排除列表中
def checkKeyInExcludeMaps(key, excludeMaps = []):
	for excludeMap in excludeMaps:
		if key in excludeMap:
			return True;
	return False;

# 获取所有文件列表中import的模块名
def getImportMap(path, excludeMaps = []):
	fileList, fileNameMap = getFileList(path);
	excludeMaps.append(fileNameMap);
	return getImportMapByFileList(fileList, excludeMaps);

# 校验import的模块
def verifyImportMap(importMap = {}):
	unImportList = [];
	for importKey in importMap:
		try:
			__import__(importKey);
		except Exception as e:
			print(e);
			importMap[importKey] = 0
			unImportList.append(importKey);
	return unImportList, importMap;

def writeJsonFile(filePath, data):
	with open(filePath, "w") as f:
		f.write(json.dumps(data, indent=4));
		f.close();

def readJsonFile(filePath):
	data = {};
	with open(filePath, "rb") as f:
		data = json.loads(f.read().decode("utf-8", "ignore"));
		f.close();
	return data;


if __name__ == '__main__':
	# 获取上一层目录
	cwd = os.getcwd();
	path = re.sub(r"\\", r"/", cwd);
	pathList = path.split("/");
	pathList.pop();
	path = "/".join(pathList)
	# 获取import的模块名列表
	excludeMaps = {
		"TemplateWindowUI": 1,
		"TemplateDialogUI": 1,
		"TemplateViewUI": 1,
	};
	ipMap = getImportMap(path, excludeMaps = [excludeMaps]);
	# 校验import的模块
	verifyImportMap(ipMap);
	# 写入Json文件
	writeJsonFile(path + "\\json\\importMap.json", ipMap);
	
	# importMap = readJsonFile(path + "\\json\\importMap.json");