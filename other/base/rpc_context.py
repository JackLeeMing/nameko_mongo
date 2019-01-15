# -*- coding:utf-8 -*-
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from nameko.standalone.rpc import ClusterRpcProxy

CONFIG = dict(AMQP_URI=__conf__.AMQP_URI)
class RPCContextHandler(object):
	"""
	base handler for session
	"""
	def _execute(self, transforms, *args, **kwargs):
		''' select base handler for self '''
		with ClusterRpcProxy(CONFIG) as rpc:
			self.rpc = rpc
			if isinstance(self, WebSocketHandler):
				WebSocketHandler._execute(self, transforms, *args, **kwargs)
			elif isinstance(self, RequestHandler):
				RequestHandler._execute(self, transforms, *args, **kwargs)

__all__ = ["RPCContextHandler"]