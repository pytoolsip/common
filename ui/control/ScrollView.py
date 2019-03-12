# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-29 22:24:58
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-10-01 17:08:42

import wx;
import math;

class ScrollView(wx.Panel):
	def __init__(self, parent, id = -1, params = {}, contentView = None):
		self.initBefore(params, contentView); # 初始化
		super(ScrollView, self).__init__(parent, id, size = self.params["size"], style = self.params["style"]);
		self.initAfter()

	def initBefore(self, params, contentView):
		# 初始化参数
		self.params = {
			"size" : (0,0),
			"style" : wx.BORDER_NONE,
			"lineUpDownDist" : 4,
			"freezeStyle" : False,
		};
		for k,v in params.items():
			self.params[k] = v;
		# 初始化contentView
		if contentView:
			self.contentView = contentView;
			self.adjustParams();

	def adjustParams(self):
		self.contentView.Reparent(self);
		contentSize = self.contentView.GetSize();
		if not self.params["freezeStyle"]:
			style = self.params["style"];
			if contentSize[0] > self.params["size"][0]:
				self.params["style"] |= wx.HSCROLL;
			if contentSize[1] > self.params["size"][1]:
				self.params["style"] |= wx.VSCROLL;

	def initAfter(self):
		if hasattr(self, "contentView"):
			self.initScrollBar();
			self.initEvents();
		else:
			if self.HasFlag(wx.HSCROLL):
				self.SetScrollbar(wx.HORIZONTAL, 0, self.GetSize()[0], -1);
			if self.HasFlag(wx.VSCROLL):
				self.SetScrollbar(wx.VERTICAL, 0, self.GetSize()[1], -1);

	def setContentView(self, contentView):
		if hasattr(self, "contentView"):
			self.contentView.Destroy();
		self.contentView = contentView;
		self.initAfter();

	def initScrollBar(self):
		self.scrollSize = [0,0];
		self.scrollRange = [0,0];
		contentSize = self.contentView.GetSize();
		selfSize = self.GetSize();
		# 水平滚动条
		if contentSize[0] > selfSize[0]:
			sizeX = math.floor(selfSize[0]*selfSize[0]/(contentSize[0]));
			self.SetScrollbar(wx.HORIZONTAL, 0, sizeX, selfSize[0]);
			self.scrollRange[0] = self.GetScrollRange(wx.HORIZONTAL) - self.GetScrollThumb(wx.HORIZONTAL);
			self.scrollSize[0] = contentSize[0] - selfSize[0];
		elif self.HasFlag(wx.HSCROLL):
			self.SetScrollbar(wx.HORIZONTAL, 0, self.GetSize()[0], -1);
		# 垂直滚动条
		if contentSize[1] > selfSize[1]:
			sizeX = math.floor(selfSize[1]*selfSize[1]/(contentSize[1]));
			self.SetScrollbar(wx.VERTICAL, 1, sizeX, selfSize[1]);
			self.scrollRange[1] = self.GetScrollRange(wx.VERTICAL) - self.GetScrollThumb(wx.VERTICAL);
			self.scrollSize[1] = contentSize[1] - selfSize[1];
		elif self.HasFlag(wx.VSCROLL):
			self.SetScrollbar(wx.VERTICAL, 0, self.GetSize()[1], -1);

	def initEvents(self):
		self.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.onScrollThumb);
		self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.onScrollLineUp);
		self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.onScrollLineDown);
		if hasattr(self, "contentView"):
			self.contentView.Bind(wx.EVT_SIZE, self.changeScrollBar);

	def changeScrollBar(self, event):
		self.initScrollBar();

	def onScrollThumb(self, event):
		self.scrollThumbTo(event.GetPosition(), event.GetOrientation());

	def scrollThumbTo(self, curViewPos, orientation):
		# 判断滚动条方向
		index = 0;
		if orientation == wx.VERTICAL:
			index = 1;
		# 获取滚动视图数据
		lastViewPos = 0;
		if hasattr(self, "lastViewPos"):
			lastViewPos = self.lastViewPos[index];
		else:
			self.lastViewPos = [0,0];
		scrollSize = self.scrollSize[index];
		scrollRange = self.scrollRange[index];
		if scrollRange > 0:
			scrollDist = scrollSize * (lastViewPos - curViewPos) / scrollRange;
			if scrollDist % 1 != 0:
				scrollDist = round(scrollDist)
				if math.fabs(scrollDist) > scrollSize:
					scrollDist = scrollSize * math.fabs(scrollDist) / scrollDist;
				curViewPos = lastViewPos - scrollDist * scrollRange / scrollSize;
			# 保存当前滚动条位置
			self.lastViewPos[index] = curViewPos;
			if scrollDist != 0:
				# 滚动视图
				if orientation == wx.HORIZONTAL:
					self.ScrollWindow(scrollDist, 0);
					self.SetScrollPos(wx.HORIZONTAL, curViewPos);
				else:
					self.ScrollWindow(0, scrollDist);
					self.SetScrollPos(wx.VERTICAL, curViewPos);

	def onScrollLineUp(self, event):
		# 判断滚动条方向
		orientation = event.GetOrientation();
		index = 0;
		if orientation == wx.VERTICAL:
			index = 1;
		# 获取滚动视图数据
		lastViewPos = 0;
		if hasattr(self, "lastViewPos"):
			lastViewPos = self.lastViewPos[index];
		curViewPos = lastViewPos - self.params["lineUpDownDist"];
		if curViewPos >= 0:
			self.scrollThumbTo(curViewPos, orientation);
		elif lastViewPos >= 0:
			self.scrollThumbTo(0, orientation);

	def onScrollLineDown(self, event):
		# 判断滚动条方向
		orientation = event.GetOrientation();
		index = 0;
		if orientation == wx.VERTICAL:
			index = 1;
		# 获取滚动视图数据
		lastViewPos = 0;
		if hasattr(self, "lastViewPos"):
			lastViewPos = self.lastViewPos[index];
		curViewPos = lastViewPos + self.params["lineUpDownDist"];
		if curViewPos <= self.scrollRange[index]:
			self.scrollThumbTo(curViewPos, orientation);
		elif lastViewPos <= self.scrollRange[index]:
			self.scrollThumbTo(self.scrollRange[index], orientation);