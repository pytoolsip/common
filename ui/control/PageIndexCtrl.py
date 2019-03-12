# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-29 22:24:58
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-12 16:50:32

import wx;

class PageIndexCtrl(wx.Panel):
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(PageIndexCtrl, self).__init__(parent, id, size = self.__params["size"]);
		self.itemKeyDict = {};
		self.createControls();
		self.initViewLayout();
		self.resetForegroundColor();
		self.createTimers();
		self.currentItem = None;
		# self.SetBackgroundColour(wx.Colour(0,0,0))

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.stopAllTimer(isDestroy = True); # 停止所有定时器
		pass;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : (-1,-1),
			"firstLabel" : "首页",
			"previousLabel" : "上一页",
			"nextLabel" : "下一页",
			"lastLabel" : "末尾",
			"skipLabel" : "跳转",
			"inputSize" : (30,18),
			"disenableColor" : wx.Colour(180,180,180),
			"blursColor" : wx.Colour(60,60,60),
			"focusColor" : wx.Colour(0,180,0),
			"totalCount" : 1,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def createControls(self):
		self.createFirst();
		self.createPrevious();
		self.createCurIndex();
		self.createTotalText();
		self.createNext();
		self.createLast();
		self.createInput();
		self.createSkip();
		pass;

	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.first, proportion = 0, flag = wx.RIGHT, border = 4);
		box.Add(self.previous, proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 4);
		box.Add(self.curIndex, proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.totalText, proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.next, proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 4);
		box.Add(self.last, proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 4);
		box.Add(self.input, proportion = 0, flag = wx.LEFT|wx.RIGHT, border = 8);
		box.Add(self.skip, proportion = 0, flag = wx.LEFT, border = 0);
		self.SetSizerAndFit(box);

	def createFirst(self):
		self.first = wx.StaticText(self, label = self.__params["firstLabel"]);
		self.first.SetForegroundColour(self.__params["blursColor"]);
		self.bindEvent(self.first, "First");

	def createPrevious(self):
		self.previous = wx.StaticText(self, label = self.__params["previousLabel"]);
		self.previous.SetForegroundColour(self.__params["blursColor"]);
		self.bindEvent(self.previous, "Previous");

	def createCurIndex(self):
		self.curIndex = wx.StaticText(self, label = "1");
		self.curIndex.SetForegroundColour(self.__params["disenableColor"]);

	def createTotalText(self):
		self.totalText = wx.StaticText(self, label = "共" + str(self.getTotalCount()) + "页");
		self.totalText.SetForegroundColour(self.__params["disenableColor"]);

	def createNext(self):
		self.next = wx.StaticText(self, label = self.__params["nextLabel"]);
		self.next.SetForegroundColour(self.__params["blursColor"]);
		self.bindEvent(self.next, "Next");

	def createLast(self):
		self.last = wx.StaticText(self, label = self.__params["lastLabel"]);
		self.last.SetForegroundColour(self.__params["blursColor"]);
		self.bindEvent(self.last, "Last");

	def createInput(self):
		self.input = wx.TextCtrl(self, -1, value = "", size = self.__params["inputSize"]);

	def createSkip(self):
		self.skip = wx.StaticText(self, label = self.__params["skipLabel"]);
		self.skip.SetForegroundColour(self.__params["blursColor"]);
		self.bindEvent(self.skip, "Skip");

	def bindEvent(self, item, key):
		if isinstance(key, str) and key != "":
			self.itemKeyDict[item.GetId()] = key;
			item.Bind(wx.EVT_ENTER_WINDOW, self.onEnterItem);
			item.Bind(wx.EVT_LEFT_DOWN, self.onClickItem);
		
	def createTimers(self):
		# 创建显示提示定时回调
		self.updateItemFgColorTimer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onUpdateItemFgColorTimer, self.updateItemFgColorTimer);

	def stopAllTimer(self, isDestroy = False):
		if hasattr(self, "updateItemFgColorTimer") and self.updateItemFgColorTimer.IsRunning():
			self.updateItemFgColorTimer.Stop();
			if isDestroy:
				del self.updateItemFgColorTimer;

	# 更新前景颜色
	def updateForegroundColor(self, item, wxColor):
		if item.GetForegroundColour() != wxColor and item.SetForegroundColour(wxColor):
			item.Refresh();
			self.resetForegroundColor();

	def isPointInRect(self, pos):
		return self.isPointInItemRect(pos);

	def isPointInItemRect(self, pos, item = None):
		item = item or self
		# 转换位置
		convertPos = item.ScreenToClient(*pos);
		# 判断位置
		if convertPos[0] >= 0 and convertPos[0] <= item.GetSize()[0] and convertPos[1] >= 0 and convertPos[1] <= item.GetSize()[1]:
			return True;
		return False;

	def onEnterItem(self, event):
		if self.currentItem != event.GetEventObject():
			if self.currentItem:
				self.updateForegroundColor(self.currentItem, self.__params["blursColor"]);
			self.currentItem = event.GetEventObject(); # 重置当前Item
			self.updateForegroundColor(self.currentItem, self.__params["focusColor"]);
			self.updateItemFgColorTimer.Start(100); # 启动更新背景颜色定时器
		
	def onUpdateItemFgColorTimer(self, event):
		if not self.isPointInItemRect(wx.GetMousePosition(), item = self.currentItem): # 判断鼠标位置是否在节点内
			self.updateForegroundColor(self.currentItem, self.__params["blursColor"]);
			self.currentItem = None;
			self.updateItemFgColorTimer.Stop();

	def onClickItem(self, event):
		if event.GetEventObject().GetForegroundColour() != self.__params["disenableColor"]:
			objId = event.GetEventObject().GetId();
			if objId in self.itemKeyDict:
				curIdx = self.getCurIndex();
				if self.itemKeyDict[objId] == "First":
					self.setCurIndex(0);
				elif self.itemKeyDict[objId] == "Previous":
					if curIdx > 1:
						self.setCurIndex(curIdx - 1);
				elif self.itemKeyDict[objId] == "Next":
					if curIdx < self.getTotalCount():
						self.setCurIndex(curIdx + 1);
				elif self.itemKeyDict[objId] == "Last":
					self.setCurIndex(self.getTotalCount());
				elif self.itemKeyDict[objId] == "Skip":
					val = self.input.GetValue()
					try:
						idx = int(val);
						if idx > 0 and idx <self.getTotalCount():
							self.setCurIndex(idx);
					except Exception:
						wx.TipWindow(self, "输入不允许包含非数字！");
				if hasattr(self, "on" + self.itemKeyDict[objId]):
					getattr(self, "on" + self.itemKeyDict[objId])(self, event);

	def setCurIndex(self, curIdx):
		if isinstance(curIdx, int) and curIdx > 0 and self.getCurIndex() != curIdx:
			# 重置当前Index
			self.curIndex.SetLabel(str(curIdx));
			# 根据curIdx更新ForegroundColor
			self.resetForegroundColor()
			# 调用改变改变index的回调函数
			if hasattr(self, "onChangeIndex"):
				self.onChangeIndex(curIdx);

	def resetForegroundColor(self):
		curIdx = self.getCurIndex();
		# 判断当前index是否为1【首页】
		if curIdx == 1:
			self.updateForegroundColor(self.previous, self.__params["disenableColor"]);
		elif self.previous.GetForegroundColour() == self.__params["disenableColor"]:
			self.updateForegroundColor(self.previous, self.__params["blursColor"]);
		# 判断当前index是否为totalCount【尾页】
		if curIdx == self.getTotalCount():
			self.updateForegroundColor(self.next, self.__params["disenableColor"]);
		elif self.next.GetForegroundColour() == self.__params["disenableColor"]:
			self.updateForegroundColor(self.next, self.__params["blursColor"]);

	def getCurIndex(self):
		return int(self.curIndex.GetLabel());

	def setTotalCount(self, count):
		if isinstance(count, int) and count > 0:
			self.__params["totalCount"] = count;
			self.totalTextSetLabel("共" + str(self.getTotalCount()) + "页");

	def getTotalCount(self):
		return self.__params["totalCount"];
