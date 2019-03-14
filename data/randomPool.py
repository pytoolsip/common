# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2018-11-08 15:09:55
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 18:10:26

import random;

class RandomPool(object):
	"""docstring for RandomPool"""
	def __init__(self, varList = []):
		super(RandomPool, self).__init__()
		self.setVarList(varList);

	def setVarList(self, varList = []):
		self.__varList = [];
		if not isinstance(varList, list):
			varList = [];
		# 拷贝varList到self.__varList
		self.mergeList(self.__varList, varList, isCopy = True);
		self.t_varList = [];

	def getVarList(self, count):
		varList = [];
		# 合并数据
		if len(self.__varList) < count:
			# 合并self.t_varList的所有数据到self.__varList
			self.mergeList(self.__varList, self.t_varList);
		# 打乱数据
		random.shuffle(self.__varList);
		# 合并count个self.__varList中的数据到varList
		self.mergeList(varList, self.__varList, count = count);
		# 拷贝varList到self.t_varList
		self.mergeList(self.t_varList, varList, isCopy = True);
		return varList;

	def mergeList(self, sL, tL, count = 0, isCopy = False):
		if count == 0 or count > len(tL):
			count = len(tL);
		for i in range(0,count):
			if isCopy:
				sL.append(tL[i]);
			else:
				sL.append(tL.pop(0));

		
if __name__ == '__main__':
	try:
		RP = RandomPool([1,2,3,4,5,6,7,8,9])
		for i in range(1,10):
			print(RP.getVarList(3))
	except Exception as e:
		print(e)