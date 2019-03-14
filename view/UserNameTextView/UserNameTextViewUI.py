# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 22:27:47
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 19:00:41

import wx;

from _Global import _GG;
from function.base import *;

class UserNameTextViewUI(wx.Panel):
	"""docstring for UserNameTextViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None):
		super(UserNameTextViewUI, self).__init__(parent, id);
		self.className_ = UserNameTextViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		self.createTitleText();
		self.createUserNameText();
		pass;
		
	def initViewLayout(self):
		hbox = wx.BoxSizer(wx.HORIZONTAL);
		hbox.Add(self.userTitleText, 0);
		hbox.Add(self.userNameText, 0);
		self.SetSizer(hbox);
		pass;

	def updateView(self, data):
		pass;

	def createTitleText(self):
		# 创建文本
		self.userTitleText = wx.StaticText(self, -1, u"当前用户:  ", style = wx.ALIGN_LEFT);
		titleFont = wx.Font(8, wx.DECORATIVE, wx.NORMAL, wx.BOLD);
		self.userTitleText.SetFont(titleFont);
		# self.userTitleText.SetForegroundColour(wx.Colour(108,108,108));

	def createUserNameText(self):
		userName = self.getCtr().getCurUserName();
		self.userNameText = wx.StaticText(self, -1, userName, style = wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_ELLIPSIZE_END);
		titleFont = wx.Font(8, wx.DECORATIVE, wx.NORMAL, wx.BOLD);
		self.userNameText.SetFont(titleFont);
		self.userNameText.SetForegroundColour(wx.Colour(60,120,60));
