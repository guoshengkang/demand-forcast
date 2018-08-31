#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-06 15:02:11
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

# 导入非自定义的包
import demjson
import pandas as pd
import datetime
# 导入自定义的包 algorithm.demand_forecast.
from intelligent_model import *
from nonintelligent_model import *


class DemandForecastAlgorithm():
	def __init__(
		self, 
		# True/False类型
		isIntelligent=False,
		# json字符串类型
		input_data_str=None,
		# json字符串类型
		time_data_str=None,
		# 字符串类型
		date_start=None,
		# 字符串类型
		date_end=None,
		# 字典类型
		time2market=None,
		# 类表类型
		forcast_models = ['WMA'],
		# 字典类型
		evaluation = 'MAPE',
		# int类型
		length_merge=1,
		# int类型
		period=7):
		self.isIntelligent=isIntelligent
		self.date_start=datetime.datetime.strptime(date_start,'%Y-%m-%d')
		self.date_end=datetime.datetime.strptime(date_end,'%Y-%m-%d')
		# json字符串转成字典列表
		json_list = demjson.decode(input_data_str)
		# pd读取字典列表
		df_input_data=pd.DataFrame(json_list)
		# 将date字符串转化日期类型
		df_input_data['date'] = df_input_data['date'].map(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d')) #将字符串
		self.input_data_df=df_input_data
		# json字符串转成字典列表
		json_list = demjson.decode(time_data_str)
		# pd读取字典列表
		df_time_data=pd.DataFrame(json_list)
		# 将date字符串转化日期类型
		df_time_data['date'] = df_time_data['date'].map(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d')) #将字符串
		self.config_data_df=df_time_data
		self.time2market=time2market
		self.forcast_models=forcast_models
		self.evaluation=evaluation
		self.length_merge=length_merge
		self.period=period

	def run(self):
		if self.isIntelligent:
			result_json=intelligent_model(
				input_data_df=self.input_data_df,
				config_data_df=self.config_data_df,
				date_start=self.date_start,
				date_end=self.date_end,
				time2market=self.time2market,
				forcast_model=self.forcast_models,
				evaluation=self.evaluation,
				length_merge=self.length_merge,
				period=self.period)
		else:
			result_json=nonintelligent_model(
				input_data_df=self.input_data_df,
				config_data_df=self.config_data_df,
				date_start=self.date_start,
				date_end=self.date_end,
				time2market=self.time2market,
				forcast_model=self.forcast_models[0],
				evaluation=self.evaluation,
				length_merge=self.length_merge,
				period=self.period)
		return result_json
