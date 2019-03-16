# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-06-06 22:52:21
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-03-16 15:09:23

from _Global import _GG;
from function.base import *;
BaseBehavior = _GG("BaseBehavior");

import re;

try:
	import xml.etree.cElementTree as ET;
except ImportError:
	import xml.etree.ElementTree as ET;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"getElementTreesByFilePath" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		# {
		# 	"path" : "tempBehavior", 
		# 	"basePath" : _GG("g_CommonPath") + "behavior/",
		# },
	];

class XmlConfigParseBehavior(BaseBehavior):
	def __init__(self):
		super(XmlConfigParseBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = XmlConfigParseBehavior.__name__;
		pass;

	# 根据文件路径，获取元素树对象
	def getElementTreesByFilePath(self, obj, filePath, _retTuple = None):
		if not re.search(r".+\.xml$", filePath):
			_GG("Log").e("The params of filePath has error!");
		else:
			return ET.parse(filePath);
