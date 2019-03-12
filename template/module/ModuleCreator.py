# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-05 13:08:49
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-12 10:22:55


import linecache;
import getpass;
import time;
import os;
import re;
try:
	import tkinter as Tkinter;
except Exception:
	import Tkinter as Tkinter;
	import tkMessageBox as Messagebox;
else:
	import tkinter.messagebox as Messagebox;


class CreateModuleObj(object):
	"""docstring for CreateModuleObj"""
	def __init__(self, moduleName):
		super(CreateModuleObj, self).__init__();
		self.modulePath = os.getcwd() + "\\module\\";
		self.moduleName = moduleName;
		self.userName = self.getUserName();
		self.fileHeadConfig = self.initFileHeadConfig();

	def createMod(self, targetName, targetPath = ""):
		if len(targetPath) > 0:
			isCreateFile,targetFilePath = self.checkAndCreateFilePath(targetPath, targetName);
			if isCreateFile == True:
				self.createFilesByRecursion(targetFilePath, targetName, self.modulePath, self.getModuleFullName());
		else:
			raise Exception("The Param named \"targetPath\" is invalid value!");

	def initFileHeadConfig(self):
		return {
			"@Author" : "getUserName",
			"@Date" : "getNowDate",
			"@Last Modified by" : "getUserName",
			"@Last Modified time" : "getNowDate",
		};

	def getFileHeadReplacedContent(self, line):
		for Key,Func in self.fileHeadConfig.items():
			if re.search(r""+Key, line):
				return False, self.getReplacedStr(Key, getattr(self, Func)(), line);
		if re.search("^[def,class].*", line):
			return True, line;
		return False, line;

	def getReplacedStr(self, findStr, replaceStr, content):
		regStr = re.compile(".*"+findStr+"[:]\s*(.+)\s*$");
		findRet = re.findall(regStr, content);
		return re.sub(r""+findRet[0], r""+replaceStr, content);

	def getUserName(self):
		if hasattr(self, "userName"):
			return self.userName;
		return getpass.getuser();

	def getNowDate(self):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()));

	def getPathByRelativePath(self, path, basePath = ""):
		if len(basePath) == 0:
			basePath = os.getcwd();
		basePath = re.sub(r"/", r"\\", basePath);
		basePathList = basePath.split("\\");
		path = re.sub(r"/", r"\\", path);
		pathList = path.split("\\");
		while len(pathList) > 0:
			if pathList[0] == "..":
				basePathList.pop();
				pathList.pop(0);
			else:
				basePathList.extend(pathList);
				break;
		return "\\".join(basePathList).strip();

	def getModuleFullName(self):
		if os.path.isdir(self.modulePath + self.moduleName):
			return self.moduleName;
		else:
			return self.moduleName + ".py";

	def checkAndCreateFilePath(self, targetPath, targetName):
		# 检测目标文件是否已存在
		targetModPath = self.getPathByRelativePath(targetPath);
		targetFileFulName = targetModPath + targetName;
		if not os.path.isdir(self.modulePath + self.moduleName):
			targetFileFulName += ".py";
		if os.path.exists(targetFileFulName):
			# isCreateFile = self.checkAndShowQuestionMsg("询问消息", "已存在所要创建的文件，是否要覆盖！！？");
			isCreateFile = self.checkAndShowWarningMsg("警告消息", "已存在所要创建的文件！！！");
			if not isCreateFile:
				return False, "";
		# 若文件所在路径不存在，则创建相应路径
		if not os.path.exists(targetModPath):
			os.makedirs(targetModPath);
		return True, targetModPath;

	def createFilesByRecursion(self, targetFilePath, targetFileName, moduleFilePath, moduleFileName):
		if os.path.isdir(moduleFilePath + moduleFileName):
			newTargetFilePath = self.checkAndCreateFolderByModule(targetFilePath, moduleFileName, targetFileName);
			listdir = os.listdir(moduleFilePath + moduleFileName);
			for fileName in listdir:
				self.createFilesByRecursion(newTargetFilePath, targetFileName, moduleFilePath + moduleFileName + "\\", fileName);
		else:
			self.createFileByModule(targetFilePath, targetFileName, moduleFilePath, moduleFileName);
			pass;

	def checkAndCreateFolderByModule(self, baseFilePath, filePathName, targetFileName):
		newFilePathName = re.sub(r""+self.moduleName, r""+targetFileName, filePathName);
		targetFullPath = baseFilePath + newFilePathName + "\\";
		if not os.path.exists(targetFullPath):
			os.makedirs(targetFullPath);
		return targetFullPath;

	def createFileByModule(self, targetFilePath, targetFileName, moduleFilePath, moduleFileName):
		# 获取目标文件内容
		data = "";
		isInitedFileHead = False;
		newModuleName = self.moduleName[0].upper() + self.moduleName[1:];
		for line in linecache.getlines(moduleFilePath + moduleFileName):
			newLine = line;
			if not isInitedFileHead:
				isInitedFileHead, newLine = self.getFileHeadReplacedContent(line);
				pass;
			if isInitedFileHead:
				if re.search(r"Template" + newModuleName, line):
					newLine = re.sub(r"Template" + newModuleName, r""+targetFileName, line);
					pass;
			data += newLine;
		# 写入目标文件
		targetFileFullName = targetFilePath + re.sub(r""+self.moduleName, r""+targetFileName, moduleFileName);
		try:
			with open(targetFileFullName, "w+", encoding = "utf-8") as f:
				f.writelines(data);
		except Exception:
			with open(targetFileFullName, "wb+") as f:
				f.writelines(data);
		print("It is finish to create \"{0}\" by module named \"{1}\".".format(targetFileName, moduleFileName));
		pass;

	def checkAndShowQuestionMsg(self, title, msg):
		tkTop = Tkinter.Tk();
		tkTop.withdraw()
		return Messagebox.askokcancel(title, msg);

	def checkAndShowWarningMsg(self, title, msg):
		tkTop = Tkinter.Tk();
		tkTop.withdraw()
		Messagebox.showwarning(title, msg);
		return False;