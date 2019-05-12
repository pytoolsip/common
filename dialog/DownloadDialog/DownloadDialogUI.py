# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2019-03-07 20:49:03
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:42

import wx;
import time;

from _Global import _GG;
from function.base import *;

class DownloadDialogUI(wx.Dialog):
	"""docstring for DownloadDialogUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(DownloadDialogUI, self).__init__(parent, id, title = self.__params["title"], pos = self.__params.get("pos", (0,0)), size = self.__params["size"], style = self.__params["style"]);
		self._className_ = DownloadDialogUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.Bind(wx.EVT_CLOSE, self.onClose); # 绑定关闭事件
		self.__totalSize = -1;
		self.__speedSize = 0;
		self.__startTime = time.time(); # 开始下载时间
		self.createTimer();

	def __del__(self):
		self.stopTimer(True);

	def onClose(self, event):
		self.EndModal(wx.ID_CANCEL);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"title" : "下载",
			"size" : (-1,-1),
			"style" : wx.DEFAULT_DIALOG_STYLE,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initDialog(self):
		self.createControls(); # 创建控件
		self.initDialogLayout(); # 初始化布局
		self.updatePosition(); # 更新位置

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***Dialog"); # , parent = self, params = {}
		self.createGauge();
		self.createSpeed();
		self.createSchedule();
		
	def initDialogLayout(self):
		pass;

	def updatePosition(self):
		if "pos" not in self.__params:
			winCenterPoint = _GG("WindowObject").GetMainWindowCenterPoint();
			self.SetPosition(wx.Point(winCenterPoint.x - self.GetSize()[0]/2, winCenterPoint.y - self.GetSize()[1]/2));

	def updateDialog(self, data):
		if "size" in data:
			self.update(data["size"]);

	def resetDialog(self):
		if not self.__timer.IsRunning():
			self.updateGauge(0);
			self.updateSpeed(0);
			self.__schedule.SetLabel("已下载：--/--");
			self.__totalSize = -1;
			self.__speedSize = 0;
		pass;

	def createTimer(self):
		self.__timer = _GG("TimerManager").createTimer(self, callback = self.onTimerEvent);

	def startTimer(self):
		if not self.__timer.IsRunning():
			self.__timer.Start(1000);

	def stopTimer(self, isDestroy = False):
		if self.__timer.IsRunning():
			self.__timer.Stop();
		if isDestroy:
			_GG("TimerManager").deleteTimer(self.__timer);

	def onTimerEvent(self, event = None):
		self.updateSpeed(self.__speedSize);
		self.__speedSize = 0;

	def createGauge(self):
		self.__gauge = wx.Gauge(self, size = (self.GetSize()[0], 20), style = wx.GA_SMOOTH);

	def createSpeed(self):
		self.__speed = wx.StaticText(self, label = "0B/s", style = wx.ALIGN_LEFT);

	def createSchedule(self):
		self.__schedule = wx.StaticText(self, label = "已下载：--/--", style = wx.ALIGN_LEFT);

	def start(self, totalSize = 0):
		if totalSize > 0:
			self.__totalSize = totalSize; # 总共下载的大小
			self.startTimer(); # 开始定时器

	def update(self, size = 0):
		self.updateSchedule(size);
		self.updateGauge(size/self.__totalSize);
		self.__speedSize += size;
		if size >= self.__totalSize:
			self.stopTimer();
			self.__speed.SetLabel("");

	def updateGauge(self, guage = 0):
		self.__gauge.SetValue(guage * self.__gauge.GetRange());

	def updateSpeed(self, speed = 0):
		self.__speed.SetLabel(self.formatSize(speed)+"/s");

	def updateSchedule(self, size):
		self.__schedule.SetLabel("已下载：%s/%s"%(self.formatSize(size), self.formatSize(self.__totalSize)));

	def formatSize(self, size):
		unit = "B";
		if size > 1024 * 1024 * 1000:
			size, unit = "%.2f" % (size/(1024 * 1024 * 1000)), "G";
		elif size > 1024 * 1000:
			size, unit = "%.2f" % (size/(1024 * 1000)), "M";
		elif size > 1000:
			size, unit = int(size/1000), "KB";
		return str(size) + unit;
