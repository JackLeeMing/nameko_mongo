# -*- coding:utf-8 -*-
"""
    author comger@gmail.com
    监测大屏相关数据逻辑接口,接单位设计
"""
import os
import datetime
import time
import math
import json
import pandas as pd
from bson import ObjectId
from kpages import app_path
# from mongo_util import MongoIns;mongo_util=MongoIns()
from nameko.rpc import rpc, RpcProxy
# from mongo_util import MongoInsTest
from nameko_mongo import NamekoMongoIns
Levels = {1:u'超上限轻度预警',2:u'超上限中度警告',3:u'超上限严重警告',-1:u'超下限轻度预警',-2:u'超下限中度警告',-3:u'超下限严重警告'}


def time_format(ddts, detail=False):
    ddts = int(ddts)
    day = int(ddts / (3600 * 24))
    ddts -= day*3600*24
    hour = int(ddts/3600)
    ddts -= hour*3600
    minute = int(ddts / 60)
    ddts -= minute*60
    second = int(ddts)
    if day:
        span_time = "{}天{}小时{}分{}秒".format(day, hour, minute, second) if detail  else "{}天前".format(day)
    elif hour:
        span_time = "{}小时{}分{}秒".format(hour, minute, second) if detail else "{}小时前".format(hour)
    elif minute:
        span_time = "{}分{}秒".format(minute, second) if detail else "{}分钟前".format(minute)
    else:
        span_time = "{}秒".format(second) if detail  else "{}秒前".format(second)
    return span_time


def time_to_timestamp(strtime):
    timeArray = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = time.mktime(timeArray)
    return timeStamp

def timestamp_to_time(timestamp):
    timeArray = time.localtime(timestamp)
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return str_time

def timestamp_to_date(timestamp):
    timeArray = time.localtime(timestamp)
    str_time = time.strftime("%m-%d", timeArray)
    return str_time


# class RedisTest(object):
# 	"""docstring for RedisTest"""
# 	name = 'redis'
# 	redis = Redis('development')
# 	@rpc
# 	def hello(self, name):
# 		self.redis.set("foo", name)
# 		return "Hello, {}!".format(name)

# 	@rpc
# 	def bye(self):
# 		name = self.redis.get("foo")
# 		return "Bye, {}!".format(name)


class AlarmChuzhi(object):
	"""一周报警处置"""
	name = 'alarm_chuzhi'
	mongo_util = NamekoMongoIns(project='sensorcmd',host='192.168.111.149:27019', dbname='sensorcmd')
	@rpc
	def projects_chuzhi_stats(self):
		"""最近7日所有桥梁预警处置统计 .ljk."""
		fields = {'name':1, 'location_lat':1, 'location_lng':1,'code_name':1,'monitor_items':1}
		projects, _= self.mongo_util.m_list('main_vsnproject',findall=True, fields=fields)
		project_map = dict((p['code_name'],p) for p in projects)
		code_names =project_map.keys() #获取所有项目
		month = datetime.datetime.now().month
		year = datetime.datetime.now().year
		day = datetime.datetime.now().day
		if day <=9:
		    day = '0{}'.format(day)
		end = time_to_timestamp('{}-{}-{} 00:00:00'.format(year, month, day))
		start = end - 24*3600*7
		tss = []
		for i in range(8):
		    tss.append(end-i*24*3600)
		tss.reverse()
		ts_sizes = zip(tss[:-1], tss[1:])
		search_cond = {'code_name':{'$in':code_names}}
		search_cond['$or'] = [{'chuzhi_ts':{'$gte': start, '$lt': end}},  {'queren_ts':{'$gte': start, '$lt': end}}, {'ts':{'$gte': start, '$lt': end}}]
		search_cond['status'] = {'$in':['1', '2', 1, 2,0 ,'0']}
		data, _ = self.mongo_util.m_list('alarm', findall=True, **search_cond)
		new_datas = []
		queren_datas = []
		chuzhi_datas = []
		for item in data:
			if str(item.get('status', 0)) == '1' and 'chuzhi_ts' in item:
				chuzhi_datas.append(item)
			if str(item.get('status', 0)) == '2' and 'queren_ts' in item:
				queren_datas.append(item)

			if str(item.get('status', 0)) == '0' and 'ts' in item:
				new_datas.append(item)

		def tss_2_ts(ts):
			dts = (ts[0]+ts[1])/2
			return dts

		def ts_2_label(dts):
			dateArray = datetime.datetime.utcfromtimestamp(dts)
			day = dateArray.day
			mmonth = dateArray.month
			return '{}/{}'.format(mmonth, day)

		data_dict = {'x':[tss_2_ts(its) for its in ts_sizes],'y0':[], 'y1':[], 'y2':[]}

		if new_datas and len(new_datas) >0:
			data_0_df = pd.DataFrame(new_datas)
			for its in ts_sizes:
				dts = tss_2_ts(its)
				new_count = data_0_df[((data_0_df['ts']>= its[0]) & (data_0_df['ts']< its[1]))]._id.count()
				if dts not in data_dict['x']:
					data_dict['x'].append(dts)
				data_dict['y0'].append(new_count)

		if queren_datas and len(queren_datas) >0:
			data_2_df = pd.DataFrame(queren_datas)
			for its in ts_sizes:
				dts = tss_2_ts(its)
				queren_count = data_2_df[((data_2_df['queren_ts']>= its[0]) & (data_2_df['queren_ts']< its[1]))]._id.count()
				if dts not in data_dict['x']:
					data_dict['x'].append(dts)
				data_dict['y1'].append(queren_count)

		if chuzhi_datas and len(chuzhi_datas) >0:
			data_1_df = pd.DataFrame(chuzhi_datas)
			for its in ts_sizes:
				dts = tss_2_ts(its)
				deal_count = data_1_df[((data_1_df['chuzhi_ts']>= its[0]) & (data_1_df['chuzhi_ts']< its[1]))]._id.count()
				if dts not in data_dict['x']:
					data_dict['x'].append(dts)
				data_dict['y2'].append(deal_count)

		tss = sorted(list(set(data_dict['x'])), key=lambda x:x)
		if tss:
			data_dict['x'] = [ts_2_label(x) for x in tss]
		return data_dict


	@rpc
	def projects_monitor(self):
		pipeline = [#以用户和项目为分组依据 按时间逆序排序 取第一个值
				{
					"$match": dict()
				},
				{
					"$project":{'ts':1, 'code_name':1,'sensor_type':1,'node_id':1,'_id':0, 'sensor_id':1}
				},
				{
					"$sort": {'ts': -1}
				},
				{
					"$group":{"_id":
					{"sensor_type":"$sensor_type", "sensor_id":"$sensor_id"},
					"time":{"$push":"$ts"},
					"node":{"$push":"$node_id"},
					"sensor_id":{"$push":"$sensor_id"}
					}
				}
				]
		new_data = self.mongo_util.m_aggregate('alarm', pipeline)
		ds = 604800 # 一周
		return new_data


class NodeMonitor(object):
	"""测点监控"""
	name="node_monitror"
	mongo_util = NamekoMongoIns(project='sensorcmd')
	@rpc
	def projects_monitor(self):
		pipeline = [#以用户和项目为分组依据 按时间逆序排序 取第一个值
				{
					"$match": dict()
				},
				{
					"$project":{'ts':1, 'code_name':1,'sensor_type':1,'node_id':1,'_id':0, 'sensor_id':1}
				},
				{
					"$sort": {'ts': -1}
				},
				{
					"$group":{"_id":
					{"sensor_type":"$sensor_type", "sensor_id":"$sensor_id"},
					"time":{"$push":"$ts"},
					"node":{"$push":"$node_id"},
					"sensor_id":{"$push":"$sensor_id"}
					}
				}
				]
		new_data = self.mongo_util.m_aggregate('alarm', pipeline)
		ds = 604800 # 一周
		return new_data