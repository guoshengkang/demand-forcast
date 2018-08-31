#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 18:03:21
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import json
import demjson
import pandas as pd
import datetime
# 导入自定义的包
from integrated_regression_model import *
from integrated_timeseries_model import *
from integrated_deeplearning_model import *

def intelligent_model(input_data_df=None,config_data_df=None,date_start=None,date_end=None,time2market=None,forecast_model='ARIMA',
	evaluation='MAPE',length_merge=2,period=5,required_data_number=5):
	'''
	非智能的预测方法
	--input parameters--
	df:预测的输入数据--df.columns=['id','date','quantity','tag_price','fact_price'] #必须列
	date_start:历史数据的开始日期--str
	date_end:历史数据的结束日期--str
	time2market:产品的上市日期--str
	test_size:测试数据的比例
	forecast_model:预测模型
	evaluation:预测评估方法
	length_merge:数据合并的天数
	period:预测的周期
	required_data_number:需要要的训练样本数据量
	'''
	# 移除重复数据
	df=input_data_df.drop_duplicates()
	df_config=config_data_df.drop_duplicates()
	# 预测天数
	predict_days=length_merge*period
	# 结果列表
	list_result=[]
	# 所有的对象id
	obj_ids=df['id'].unique() 
	# 循坏每个id
	for index_no,id in enumerate(obj_ids): 
		print('Processing %d-th sku:%s ... There are %d skus in total ...'%(index_no+1,id,len(obj_ids)))
		dict_result=dict()
		dict_result['id']=str(id) # TypeError: Object of type 'int64' is not JSON serializable
		# dict_result['model']=forecast_model
		df_tmp=df[df['id']==id] # 将id对应的所有数据取出来
		df_tmp.drop(['id'],axis=1,inplace=True)
		dict_result['class']=str(df_tmp['class'].unique()[0])
		# 删除类别列
		if 'class' in df.columns:
			df.drop(['class'],axis=1,inplace=True)

		# 删除标签列
		if 'label' in df_tmp.columns:
			df_tmp.drop(['label'],axis=1,inplace=True)

		# (2) 数据填充
		# date_market=datetime.datetime.strptime(date_market,'%Y-%m-%d')
		# date_min=max(date_start, date_market) # 最小日期数据
		# date_max=max(df_tmp['date'])  # 按预测数据来取最大日期
		date_min=datetime.datetime.strptime('2018-01-28','%Y-%m-%d')
		date_max=datetime.datetime.strptime('2018-05-02','%Y-%m-%d')
		# 填充缺失日期的数据--训练+测试数据
		df_tmp_config=df_config[(df_config['date']>=date_min) & (df_config['date']<=date_max)]  # 取出holiday和season数据
		df_tmp=pd.merge(df_tmp_config,df_tmp,left_on='date',right_on='date',how='left') # 左连接,所有日期
		df_tmp.fillna({'quantity':0,'promotion':0},inplace=True)     # 将所有缺失的quantity/promotion数据填充为0
		df_tmp=df_tmp.sort_values(by='date')     # 数据填充之前先将数据按时间排序
		df_tmp.fillna(method='ffill',inplace=True)     # 用前置项方式填充其他缺失数据
		# 对上市时间但没有销量时时有用
		df_tmp.fillna(method='bfill',inplace=True)     # 用后置项方式填充其他缺失数据

		y=pd.Series(df_tmp['quantity'].values,index=pd.date_range(date_min,date_max))
		y_train=y[:-predict_days]
		y_test=y[-predict_days:]
		sale_days=len(y_train[y_train>0])

		# (3) 数据特征分析及模型选择
		# y_df=df_tmp[['date','quantity']]
		# y_df=y_df.set_index(['date'])   # 将date列设置为索引,仍然为DataFrame
		# y_train=y_df['quantity']
		# y_train=y_train[:-predict_days] # 训练的数据的y值

		# CASE 1:有销量的数据<10天,则使用加权移动平均模型
		if sale_days<10:
			forecast_model='WMA'
		# CASE 2:有销量的数据>=10天,存在2次连续至少7天的销量均为0,则使用LSTM模型
		elif con_LSTM(y_series=y_train,zero_num=7):
			forecast_model='LSTM'
		# CASE 3:数据量>=50,且满足1阶差分+周期差分可平稳
		elif con_SARIMAX(y_series=y_train):
			forecast_model='SARIMAX'
		# CASE 4:数据量>=50,满足噪声检验且满足2阶内差分可平稳
		elif con_ARIMA(y_series=y_train):
			forecast_model='ARIMA'
		# CASE 5:默认的方法
		else:
			forecast_model='WMA'

		forecast_model='GBRT'
		# (4) 模型训练及滚动预测 integrated_deeplearning_model
		try:
			if forecast_model in regression_methods:
				y_real,y_fit,y_predict,error_fit=integrated_regression_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
			elif forecast_model in timeseries_methods:
				y_real,y_fit,y_predict,error_fit=integrated_timeseries_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
			elif forecast_model in deeplearning_methods:
				y_real,y_fit,y_predict,error_fit=integrated_deeplearning_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
			else:
				forecast_model='WMA'
				y_real,y_fit,y_predict,error_fit=integrated_timeseries_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
		# 若模型调用失败,则最后使用WMA
		except Exception as e:
			forecast_model='WMA'
			y_real,y_fit,y_predict,error_fit=integrated_timeseries_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
		# dict_result['y_real']=y_real
		# dict_result['y_fit']=y_fit
		# dict_result['y_predict']=y_predict
		# dict_result[evaluation]=error_fit
		y_test=timeseries_merge(y_test,length_merge=7)
		y_predict=timeseries_merge(y_predict,length_merge=7)
		pre_mape=1-np.abs(array(y_test)-array(y_predict))/(array(y_test)+1)
		dict_result['y_test']=list(y_test)
		dict_result['y_predict']=list(y_predict)
		dict_result['pre_mape']=list(pre_mape)
		# 最后才确定使用的预测模型
		dict_result['model']=forecast_model
		# 将id的预测结果dict_result添加到结果列表
		list_result.append(dict_result)
	# 结束循环每个id的预测
	# json_result = json.dumps(list_result)
	return list_result

########################################################################################
# 测试代码
if __name__=='__main__':
	# 导入数据
	# fin_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "input_data.csv")
	# dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
	# input_data_df=pd.read_csv(fin_path, parse_dates=['date'], date_parser=dateparse)

	# config_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "config_date_holiday_season_weekend.csv")
	# dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
	# config_data_df=pd.read_csv(config_path, parse_dates=['date'], date_parser=dateparse)
	# config_data_df.drop(['hld_label'],axis=1,inplace=True) # 删除hld_label列,直接修改

	# 数据库导入
	from get_data_from_db import *

	# 定义上市日期
	time2market="[{'44156':'2018-01-28','43791':'2018-01-28','41841':'2018-01-28','11111':'2018-01-28'}]"
	time2market = demjson.decode(time2market)[0]
	# 定义开始结束日期
	date_start='2018-01-28'
	date_end='2018-04-25'
	date_start=datetime.datetime.strptime(date_start,'%Y-%m-%d')
	date_end=datetime.datetime.strptime(date_end,'%Y-%m-%d')
	json_result=intelligent_model(input_data_df,config_data_df,date_start=date_start,date_end=date_end,time2market=time2market,
			forecast_model='LSTM',evaluation='MAPE',length_merge=4,period=7)
	text = json.loads(json_result)
	# 打印预测结果
	for x in text:
		# print(x)
		print(x['id'],x['class'],x['model'],x['pre_mape'])
