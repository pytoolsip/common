# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-02-23 21:36:25
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-13 00:48:43
import wx,json,threading;

import grpc;
from proto import common_pb2,common_pb2_grpc;

from _Global import _GG;

class CommonClient(object):
	"""docstring for CommonClient"""
	def __init__(self):
		super(CommonClient, self).__init__();
		conf = _GG("ClientConfig").Config();
		_HOST, _PORT = conf.Get("server", "host"), conf.Get("server", "port");
		print("channel =>", _HOST+':'+_PORT);
		self.__client = common_pb2_grpc.CommonStub(channel = grpc.insecure_channel(_HOST+':'+_PORT)); #客户端建立连接
		pass;

	def rawCallService(self, methodName, req, asynCallback = None):
		resp = None;
		if hasattr(self.__client, methodName):
			try:
				resp = getattr(self.__client, methodName)(req);
			except Exception as e:
				print("Failed to request server by key[{}] !".format(methodName), e);
		else:
			print("Invalid caller[{}] in client !".format(methodName));
		if callable(asynCallback):
			wx.CallAfter(asynCallback, resp);
		return resp;

	def callService(self, methodName, dataKey, data = {}, asynCallback = None):
		if not callable(asynCallback):
			return self.rawCallService(methodName, getattr(common_pb2, dataKey)(**data));
		threading.Thread(target = self.rawCallService, args = (methodName, getattr(common_pb2, dataKey)(**data), asynCallback)).start();

	# 编码bytes数据
	def encodeBytes(self, data):
		return str.encode(json.dumps(data));

	# 解码bytes数据
	def decodeBytes(self, data):
		return json.loads(bytes.decode(data));
