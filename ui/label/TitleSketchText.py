# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-08 17:02:19
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-12 16:50:34

import wx;

class TitleSketchText(wx.Panel):
	def __init__(self, parent, id = -1, params = {}):
		self.initParams(params);
		super(TitleSketchText, self).__init__(parent, id, size = self.params["size"], style = self.params["style"]);
		self.createControls();
		self.initViewLayout();
		self.bindEvents();
		self.createTimers();
		self.enterItem = None;
		self.tipWindow = None;

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
		self.params = {
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
			"title" : "标题",
			"name" : "名称",
			"detail" : "详细描述...",
		};
		for k,v in params.items():
			self.params[k] = v;

	def createControls(self):
		self.createTitleText();
		self.createNameText();
		self.createDetailText();

	def initViewLayout(self):
		hbox = wx.BoxSizer(wx.HORIZONTAL);
		hbox.Add(self.title, proportion = 0, flag = wx.TOP|wx.BOTTOM|wx.RIGHT, border = 4);
		hbox.Add(self.name, proportion = 0, flag = wx.TOP, border = 6);
		vbox = wx.BoxSizer(wx.VERTICAL);
		vbox.Add(hbox);
		vbox.Add(self.detail, proportion = 0, flag = wx.TOP|wx.BOTTOM, border = 4);
		self.SetSizer(vbox);

	def createTitleText(self):
		self.title = wx.StaticText(self, id = -1, label = self.params["title"], size = (self.Size[0]*2/3, -1), style = wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_MIDDLE);
		font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD);
		self.title.SetFont(font);

	def createNameText(self):
		remainSizeX = self.Size[0] - self.title.Size[0];
		self.name = wx.StaticText(self, id = -1, label = "[" + self.params["name"] + "]", size = (remainSizeX, -1), pos = (self.title.Size[0], 0), style = wx.ALIGN_RIGHT|wx.ST_ELLIPSIZE_MIDDLE);
		font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL);
		self.name.SetFont(font);

	def createDetailText(self):
		remainSizeY = self.Size[1] - max(self.title.Size[1], self.name.Size[1]);
		self.detail = wx.StaticText(self, id = -1, label = self.params["detail"], size = (self.Size[0], remainSizeY), style = wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_MIDDLE);
		font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL);
		self.detail.SetFont(font);

	def bindEvents(self):
		# 绑定鼠标移入事件
		self.Bind(wx.EVT_ENTER_WINDOW, self.onEnterText);
		self.title.Bind(wx.EVT_ENTER_WINDOW, self.onEnterText);
		self.name.Bind(wx.EVT_ENTER_WINDOW, self.onEnterTextItem);
		self.detail.Bind(wx.EVT_ENTER_WINDOW, self.onEnterTextItem);
		# 绑定点击事件
		self.Bind(wx.EVT_LEFT_DOWN, self.onClickText);
		self.title.Bind(wx.EVT_LEFT_DOWN, self.onClickText);
		self.name.Bind(wx.EVT_LEFT_DOWN, self.onClickText);
		self.detail.Bind(wx.EVT_LEFT_DOWN, self.onClickText);

	def onEnterTextItem(self, event):
		if event.GetEventObject().IsEllipsized():
			self.showTips(event.GetEventObject().GetLabel(), enterItem = event.GetEventObject());
		self.onEnterText(event);
	
	def createTimers(self):
		# 创建显示提示定时回调
		self.showTipsTimer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onTimerToShowTips, self.showTipsTimer);
		# 创建隐藏提示定时回调
		self.hideTipsTimer = wx.Timer(self);
		self.Bind(wx.EVT_TIMER, self.onTimerToHideTips, self.hideTipsTimer);

	def stopAllTimer(self, isDestroy = False):
		if self.showTipsTimer.IsRunning():
			self.showTipsTimer.Stop();
			if isDestroy:
				del self.showTipsTimer;
		if self.hideTipsTimer.IsRunning():
			self.hideTipsTimer.Stop();
			if isDestroy:
				del self.hideTipsTimer;

	def showTips(self, tipsText, enterItem = None):
		if isinstance(tipsText, str):
			self.tips = tipsText;
			if self.tips != "" and not self.tipWindow:
				# 隐藏提示
				self.hideTips();
				# 设置单次定时
				self.showTipsTimer.StartOnce(1000);
				# 重置enterItem
				self.enterItem = enterItem;

	def hideTips(self):
		if self.showTipsTimer.IsRunning():
			self.showTipsTimer.Stop();
		self.onTimerToHideTips();

	# 创建提示窗口
	def onTimerToShowTips(self, event = None):
		if self.isPointInRect(wx.GetMousePosition()): # 判断鼠标位置是否在节点内
			self.tipWindow = wx.TipWindow(self, self.tips);
			self.timeToHideTips(); # 定时隐藏提示

	def timeToHideTips(self):
		if self.tipWindow:
			# 设置单次定时
			self.hideTipsTimer.Start(100);

	# 销毁提示窗口
	def onTimerToHideTips(self, event = None):
		if not self.isPointInRect(wx.GetMousePosition()): # 判断鼠标位置是否在节点内
			self.enterItem = None;
			if self.hideTipsTimer.IsRunning():
				self.hideTipsTimer.Stop(); # 停止定时器
			if self.tipWindow:
				try:
					self.tipWindow.Destroy();
				except Exception as e:
					pass;
				self.tipWindow = None;

	# 更新背景颜色
	def updateBackgroundColor(self, wxColor):
		if self.SetBackgroundColour(wxColor):
			self.Refresh();

	def isPointInRect(self, pos):
		return self.isPointInItemRect(pos, item = self.enterItem);

	def isPointInItemRect(self, pos, item = None):
		item = item or self
		# 转换位置
		convertPos = item.ScreenToClient(*pos);
		# 判断位置
		if convertPos[0] >= 0 and convertPos[0] <= item.GetSize()[0] and convertPos[1] >= 0 and convertPos[1] <= item.GetSize()[1]:
			return True;
		return False;

	def onClickText(self, event):
		if hasattr(self, "onClick"):
			self.onClick(self, event);

	def onEnterText(self, event):
		if hasattr(self, "onEnter"):
			self.onEnter(self, event);