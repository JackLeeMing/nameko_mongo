# -*- coding:utf-8 -*-
from kpages import url,app_path
import pandas as pd
import numpy as np
from bson import ObjectId
from restful import BaseHandler
from base import RPCContextHandler

@url(r'/all/alarm/stats')
class ChuzhiStatsHandler(RPCContextHandler, BaseHandler):
	"""
	最近7日所有桥梁预警处置统计 .ljk.

	"""
	def get(self):
		if self.rpc:
			# 异步调用
			print self.rpc
			data_dict = self.rpc.alarm_chuzhi.projects_chuzhi_stats.call_async()
			self.write(data_dict.result())
		else:
			self.write(dict(stats=False, data='RPC Not work.'))