# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-09-12 23:38:10
# @Last Modified by:   JimZhang
# @Last Modified time: 2018-09-15 10:13:43

import wx;
import re;

class XmlLabel(wx.Panel):
	def __init__(self, parent, id = -1, size = (-1,-1), label = ""):
		super(XmlLabel, self).__init__(parent, id, size = size);
		self.setLabel(label);

	def setLabel(self, label = ""):
		labelData = self.parseLabel(label);

	def parseLabel(self, label):
		# labelData
		pass;