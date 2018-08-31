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
from algorithm.demand_forecast.integrated_regression_model import *
from algorithm.demand_forecast.integrated_timeseries_model import *
from algorithm.demand_forecast.integrated_timeseries_merge_model import *
from algorithm.demand_forecast.integrated_timeseries_exog_model import *
from algorithm.demand_forecast.integrated_deeplearning_model import *

def nonintelligent_model(
	input_data_df=None,
	config_data_df=None,
	date_start=None,
	date_end=None,
	demand_class_dict=None,
	last_predicted_error=None,
	forecast_model='ARIMA',
	evaluation='MAPE',
	length_merge=2,period=5):
	'''
	非智能的预测方法
	--input parameters--
	input_data_df:产品特征数据--df
	config_data_df:时间特征数据--df
	date_start:历史数据的开始日期--str
	date_end:历史数据的结束日期--str
	demand_class_dict:产品的需求类别--dict
	forecast_model:预测模型
	evaluation:预测评估方法
	length_merge:数据合并的天数
	period:预测的周期
	'''
	# 移除重复数据
	df=input_data_df.drop_duplicates()
	df_config=config_data_df.drop_duplicates()
	# 预测天数
	predict_days=length_merge*period
	# 训练和测试数据的开始/结束日期
	date_end_train=date_end
	date_start_predict=date_end_train+datetime.timedelta(1)
	date_end_predict=date_end_train+datetime.timedelta(predict_days)
	# 结果列表
	list_result=[]
	# 所有的对象id
	obj_ids=df['id'].unique()
	# obj_ids=obj_ids[1:2]
	# 循坏每个id
	for index_no,id in enumerate(obj_ids): 
		print('Processing {:4d}-th sku:{} ... There are {} skus in total ...'.format(index_no+1,id,len(obj_ids)))
		dict_result=dict()
		dict_result['id']=str(id) # TypeError: Object of type 'int64' is not JSON serializable
		dict_result['model']=forecast_model
		df_tmp=df[df['id']==id] # 将id对应的所有数据取出来
		df_tmp.drop(['id'],axis=1,inplace=True)
		# 训练数据的开始日期
		date_start_train=min(df_tmp['date'])
		train_sample_num=(date_end_train-date_start_train).days+1
		predict_sample_num=predict_days

		# (1) 数据检查
		# (1.1) 检查训练及测试数据是否为空
		df_train=df_tmp[df_tmp['date']<=date_end_train] #训练数据
		if df_train.empty:
			dict_result['code']=1000
			dict_result['desc']='训练数据为空'
			list_result.append(dict_result)
			print('[INFO]:训练数据为空!!!')
			continue
		df_predict=df_tmp[df_tmp['date']>date_end_train] #预测数据
		if df_predict.empty:
			dict_result['code']=1001
			dict_result['desc']='预测数据为空'
			list_result.append(dict_result)
			print('[INFO]:预测数据为空!!!')
			continue
		# (1.2) 检查训练及测试数据是否存在缺失特征数据的日期
		if len(df_train)<train_sample_num:
			dict_result['code']=1002
			dict_result['desc']='训练数据存在缺失'
			list_result.append(dict_result)
			print('[INFO]:训练数据存在缺失!!!')
			continue
		if len(df_predict)<predict_sample_num:
			dict_result['code']=1003
			dict_result['desc']='预测数据存在缺失'
			list_result.append(dict_result)
			print('[INFO]:预测数据存在缺失!!!')
			continue
		# (1.3) 检查产品需求类别数据是否存在
		demand_class=demand_class_dict.get(str(id),-1)
		if demand_class==-1:
			dict_result['code']=1004
			dict_result['desc']='缺少产品需求类别'
			list_result.append(dict_result)
			print('[INFO]:缺少产品需求类别!!!')
			continue

		# (2) 数据填充
		# 填充缺失日期的数据--训练+测试数据
		df_tmp_config=df_config[(df_config['date']>=date_start_train) & (df_config['date']<=date_end_predict)]  # 取出holiday和season数据
		df_tmp=pd.merge(df_tmp_config,df_tmp,left_on='date',right_on='date',how='left') # 左连接,所有日期
		df_tmp.fillna(0,inplace=True)     # 将所有缺失数据填充为0
		# 前项填充列,需要根据业务场景修改！！！
		ffill_cols=['sale_price','purchase_price','on_hand_quantity']
		df_tmp[ffill_cols].fillna(method='ffill',inplace=True)     # 用前置项方式填充其他缺失数据
		df_tmp.fillna(0,inplace=True)     # 将其他所有缺失数据填充为0
		
		# (3) 模型训练及滚动预测 integrated_deeplearning_model
		# 预测算法的输入参数
		parameters=dict()
		parameters['isIntelligent']=True
		parameters['sku_id']=str(id)
		parameters['df']=df_tmp
		parameters['forecast_model']=forecast_model
		parameters['evaluation']=evaluation
		parameters['length_merge']=length_merge
		parameters['period']=period
		parameters['retrain']=True
		try:
			if forecast_model in regression_methods:
				y_real,y_fit,y_predict,error_fit=integrated_regression_model(**parameters)
			elif forecast_model in timeseries_methods:
				y_real,y_fit,y_predict,error_fit=integrated_timeseries_model(**parameters)
			elif forecast_model in timeseries_exog_methods:
				y_real,y_fit,y_predict,error_fit=integrated_timeseries_exog_model(**parameters)
			elif forecast_model in timeseries_merge_methods:
				y_real,y_fit,y_predict,error_fit=integrated_timeseries_merge_model(**parameters)
			elif forecast_model in deeplearning_methods:
				y_real,y_fit,y_predict,error_fit=integrated_deeplearning_model(**parameters)	
			else:
				dict_result['code']=1005
				dict_result['desc']="找不到该模型:%s"%forecast_model
				list_result.append(dict_result)
				continue
		except Exception as e:
			print('[ERROR]:{0}模型调用失败({1})'.format(forecast_model,e))
			dict_result['error']='模型调用失败(%s)'%(e)
			list_result.append(dict_result)
			continue
		dict_result['y_real']=y_real
		dict_result['y_fit']=y_fit
		dict_result['y_predict']=y_predict
		dict_result[evaluation]=error_fit
		# 将id的预测结果dict_result添加到结果列表
		list_result.append(dict_result)
	# 结束循环每个id的预测
	# json_result = json.dumps(list_result)
	return list_result

########################################################################################
# 测试代码
if __name__=='__main__':
	# 导入数据
	fin_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "input_data.csv")
	dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
	input_data_df=pd.read_csv(fin_path, parse_dates=['date'], date_parser=dateparse)

	config_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "config_date_holiday_season_weekend.csv")
	dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
	config_data_df=pd.read_csv(config_path, parse_dates=['date'], date_parser=dateparse)
	config_data_df.drop(['hld_label'],axis=1,inplace=True) # 删除hld_label列,直接修改

	# 定义上市日期
	time2market="[{'43791':'2018-01-28','41841':'2018-01-28','11111':'2018-01-28'}]"
	time2market = demjson.decode(time2market)[0]
	# 定义开始结束日期
	date_start='2018-01-28'
	date_end='2018-04-25'
	date_start=datetime.datetime.strptime(date_start,'%Y-%m-%d')
	date_end=datetime.datetime.strptime(date_end,'%Y-%m-%d')
	json_result=nonintelligent_model(input_data_df,config_data_df,date_start=date_start,date_end=date_end,time2market=time2market,
			forecast_model='ARIMA_exog',evaluation='MAPE',length_merge=1,period=7)
	text = json.loads(json_result)
	# 打印预测结果
	for x in text:
		print(x)
# timeseries_exog_methods={'ARIMA_exog':ts_ARIMA_exog,'SARIMAX_exog':ts_SARIMAX_exog}