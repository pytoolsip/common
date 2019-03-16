# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 22:27:47
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 15:20:27

import wx;

from _Global import _GG;
from function.base import *;

class UserNameTextViewUI(wx.Panel):
	"""docstring for UserNameTextViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(UserNameTextViewUI, self).__init__(parent, id);
		self._className_ = UserNameTextViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		pass;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"name" : "点击登录",
			"onClick" : None,
			"blurColor" : wx.Colour(60,160,60),
			"focusColor" : wx.Colour(60,240,60),
		};
		for k,v in params.items():
			self.__params[k] = v;

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
		if "name" in data:
			self.updateUserName(data["name"]);
		if "onClick" in data and callable(data["onClick"]):
			self.__params["onClick"] = data["onClick"];
		pass;

	def createTitleText(self):
		# 创建文本
		self.userTitleText = wx.StaticText(self, -1, u"当前用户:  ", style = wx.ALIGN_LEFT);
		titleFont = wx.Font(8, wx.DECORATIVE, wx.NORMAL, wx.BOLD);
		self.userTitleText.SetFont(titleFont);
		# self.userTitleText.SetForegroundColour(wx.Colour(108,108,108));

	def createUserNameText(self):
		self.userNameText = wx.StaticText(self, -1, self.__params["name"], style = wx.ALIGN_CENTRE_HORIZONTAL|wx.ST_ELLIPSIZE_END);
		titleFont = wx.Font(8, wx.DECORATIVE, wx.NORMAL, wx.BOLD);
		self.userNameText.SetFont(titleFont);
		self.userNameText.SetForegroundColour(self.__params["blurColor"]);
		self.userNameText.Bind(wx.EVT_ENTER_WINDOW, self.onEnterNameText);
		self.userNameText.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaveNameText);
		self.userNameText.Bind(wx.EVT_LEFT_DOWN, self.onClickNameText);

	def onEnterNameText(self, event):
		event.GetEventObject().SetForegroundColour(self.__params["focusColor"]);
		event.GetEventObject().Refresh();

	def onLeaveNameText(self, event):
		event.GetEventObject().SetForegroundColour(self.__params["blurColor"]);
		event.GetEventObject().Refresh();

	def onClickNameText(self, event):
		if callable(self.__params["onClick"]):
			self.__params["onClick"](event);

	def updateUserName(self, name):
		self.userNameText.SetLabel(name);