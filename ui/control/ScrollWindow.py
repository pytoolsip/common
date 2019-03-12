# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-29 22:24:58
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-01-12 09:45:33

import wx;

class ScrollWindow(wx.ScrolledWindow):
	"""docstring for ScrollWindow"""
	def __init__(self, parent, id = -1, params = {}, contentView = None):
		self.initParams(params);
		super(ScrollWindow, self).__init__(parent, id, size = self.__params["size"]);
		self.setContentView(contentView);
		
	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : (0,0),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def setContentView(self, contentView):
		if not contentView:
			contentView = wx.Panel(self, size = self.__params["size"]);
		# 销毁原有内容节点
		if hasattr(self, "contentView"):
			self.contentView.Destroy();
		# 重置父节点
		if contentView.Parent != self:
			contentView.Reparent(self);
		# 重置self.contentView
		self.contentView = contentView;
		# 调整滚动条
		self.adjustScrollbars();
		# 初始化事件
		self.initContentViewEvents();

	def adjustScrollbars(self, event = None):
		contentSize = self.contentView.GetSize();
		self.SetScrollbars(1, 1, contentSize[0], contentSize[1]);

	def initContentViewEvents(self):
		if hasattr(self, "contentView"):
			self.contentView.Bind(wx.EVT_SIZE, self.adjustScrollbars);
