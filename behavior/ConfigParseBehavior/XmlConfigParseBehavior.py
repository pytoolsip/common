# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-06-06 22:52:21
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-08-25 05:13:58

from _Global import _GG;
from function.base import *;
BaseBehavior = _GG("BaseBehavior");

import re;

try:
	import xml.etree.cElementTree as ET;
except ImportError:
	import xml.etree.ElementTree as ET;

def getExposeData():
	return {
		# "exposeDataName" : {},
	};

def getExposeMethod(DoType):
	return {
		"getElementTreesByFilePath" : DoType.AddToRear,
	};

class XmlConfigParseBehavior(BaseBehavior):
	def __init__(self, depends = []):
		super(XmlConfigParseBehavior, self).__init__(depends);
		self.className_ = XmlConfigParseBehavior.__name__;
		self.getExposeData = getExposeData; # 获取暴露出的数据
		self.getExposeMethod = getExposeMethod; # 获取暴露出的方法接口
		pass;

	# 根据文件路径，获取元素树对象
	def getElementTreesByFilePath(self, obj, filePath, _retTuple = None):
		if not re.search(r".+\.xml$", filePath):
			print("The params of filePath has error!");
		else:
			return ET.parse(filePath);
