# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2020-02-28 16:29:02
# @Last Modified by:   Administrator
# @Last Modified time: 2020-02-28 16:29:02
import os;
import wx;

from _Global import _GG;

from ScreenshotDialogUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		# G_EVENT.TO_UPDATE_VIEW : "updateDialog",
	};

fileFormatCfg = {
	".png" : wx.BITMAP_TYPE_PNG,
	".jpg" : wx.BITMAP_TYPE_JPEG,
	".gif" : wx.BITMAP_TYPE_GIF,
	".ico" : wx.BITMAP_TYPE_ICO,
	".bmp" : wx.BITMAP_TYPE_BMP,
	".tif" : wx.BITMAP_TYPE_TIF,
}

class ScreenshotDialogCtr(object):
	"""docstring for ScreenshotDialogCtr"""
	def __init__(self, parent, params = {}):
		super(ScreenshotDialogCtr, self).__init__();
		self._className_ = ScreenshotDialogCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent, params); # 初始化视图UI
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.initPopupMenu(); # 初始化弹出菜单

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unregisterEventMap(); # 注销事件
		self.unbindBehaviors(); # 解绑组件
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent, params):
		# 创建视图UI类
		self.__ui = ScreenshotDialogUI(parent, curPath = self._curPath, viewCtr = self, params = params);
		self.__ui.initDialog();

	def getUI(self):
		return self.__ui;

	"""
		key : 索引所创建控制类的key值
		path : 所创建控制类的路径
		parent : 所创建控制类的UI的父节点，默认为本UI
		params : 扩展参数
	"""
	def createCtrByKey(self, key, path, parent = None, params = {}):
		if not parent:
			parent = self.getUI();
		self.__CtrMap[key] = CreateCtr(path, parent, params = params);

	def getCtrByKey(self, key):
		return self.__CtrMap.get(key, None);

	def getUIByKey(self, key):
		ctr = self.getCtrByKey(key);
		if ctr:
			return ctr.getUI();
		return None;
		
	def registerEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").register(eventId, self, callbackName);

	def unregisterEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").unregister(eventId, self, callbackName);

	def bindBehaviors(self):
		pass;
		
	def unbindBehaviors(self):
		pass;
			
	def updateDialog(self, data):
		self.__ui.updateDialog(data);
	
	def onSave(self, event):
		dlg = wx.FileDialog(self.getUI(), "保存截屏图片", defaultFile = "screenshot", wildcard = "PNG files (.png)|.png|JPEG files (.jpg)|.jpg|GIF files (.gif)|.gif|ICO files (.ico)|.ico|BMP files (.bmp)|.bmp|TIF files (.tif)|.tif", style=wx.FD_SAVE);
		if dlg.ShowModal() == wx.ID_OK:
			filePath = dlg.GetPath();
			_, ext = os.path.splitext(filePath);
			if ext in fileFormatCfg:
				self.getUI().saveAs(filePath, fileFormatCfg[ext]);
			else:
				self.getUI().showMessageDialog(f"保存截屏图片（{filePath}）文件格式错误！", "保存截屏图片", style = wx.OK|wx.ICON_ERROR);
		pass;
	
	def onFullScreen(self, event):
		self.getUI().fullScreenSelectedArea();
	
	def onCancel(self, event):
		self.getUI().resetSelectedArea();

	def initPopupMenu(self):
		self.getCtrByKey("PopupMenuViewCtr").createNewMenu("Screenshot", {"itemsData" : [
			{
				"title" : "保存",
				"callback" : self.onSave,
			},
			{
				"isSeparator" : True,
			},
			{
				"title" : "全屏截图",
				"callback" : self.onFullScreen,
			},
			{
				"isSeparator" : True,
			},
			{
				"title" : "取消",
				"callback" : self.onCancel,
			},
		]});
	
	def onPopupMenu(self, pos):
		popupMenu = self.getCtrByKey("PopupMenuViewCtr").getMenu("Screenshot");
		if popupMenu:
			self.getUI().PopupMenu(popupMenu, pos);
		pass;