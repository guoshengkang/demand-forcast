#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-06 15:53:45
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import json
import demjson
import pandas as pd
from peewee import Model,PostgresqlDatabase
from playhouse.pool import PooledPostgresqlDatabase
from datetime import datetime
from demand_forecast_algorithm import *

db = PooledPostgresqlDatabase(database='ios2',
                              host='172.12.78.217',
                              port=5432,
                              user='postgres',
                              password='Password123',
                              max_connections=20,    # 可省略
                              stale_timeout=300,     # 可省略
                             )

class BaseModel(Model):
    class Meta:
        database = db

config_sql='''
	SELECT
	work_day AS date,
	holiday_type AS holiday,
	month AS season,
	is_weekend AS weekend
	FROM 
	ios_base_work_calendar
	'''
sql_results = BaseModel.raw(config_sql)
time_data = []
for result in sql_results:
    data_dict = dict()
    data_dict['date'] = str(result.date)
    data_dict['holiday'] = str(result.holiday)
    data_dict['season'] = str(result.season)
    data_dict['weekend'] = int(result.weekend)
    time_data.append(data_dict)
# 转成json字符串
time_data_str=str(time_data)

sql='''
	SELECT *
	FROM input_data
	'''

sql_results = BaseModel.raw(sql)
input_data = []
for result in sql_results:
    data_dict = dict()
    data_dict['id'] = int(result.id)
    data_dict['date'] = str(result.date)
    data_dict['quantity'] = int(result.quantity)
    data_dict['tag_price'] = round(float(result.tag_price), 2)
    data_dict['fact_price'] = round(float(result.fact_price), 2)
    data_dict['discount'] = round(float(result.discount), 2)
    data_dict['promotion'] = int(result.promotion)
    data_dict['class'] = int(result.classification_level)
    data_dict['label'] = int(result.label)  # 0表示训练数据
    input_data.append(data_dict)
# 转成json字符串
input_data_str=str(input_data)

# 定义上市日期
time2market="[{'43791':'2018-01-28','41841':'2018-01-28','11111':'2018-01-28'}]"
time2market = demjson.decode(time2market)[0]
# 定义开始结束日期
date_start='2018-01-28'
date_end='2018-04-25'

cdf=DemandForecastAlgorithm(
	isIntelligent=True,
    date_start=date_start,
    date_end=date_end,
    input_data_str=input_data_str,
    time_data_str=time_data_str,
    time2market=time2market,
    forcast_models=['GBRT'],
    evaluation='MAPE',
    length_merge=1,
    period=7)
json_result=cdf.run()

text = json.loads(json_result)
# 打印预测结果
for x in text:
	print(x)