# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-29 22:19:40
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:45:55

import wx;

from _Global import _GG;
from function.base import *;

class TemplateViewUI(wx.Panel):
	"""docstring for TemplateViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(TemplateViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self._className_ = TemplateViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_NONE,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		pass;
		
	def initViewLayout(self):
		pass;

	def updateView(self, data):
		pass;