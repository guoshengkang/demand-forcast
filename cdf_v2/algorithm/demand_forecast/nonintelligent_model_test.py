#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 18:03:21
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import json
import demjson
import pandas as pd
import datetime
from pandas.tseries.offsets import Day
# 导入自定义的包
from integrated_regression_model import *
from integrated_cnn_model import *
from integrated_timeseries_model import *
from integrated_timeseries_exog_model import *
from integrated_deeplearning_model import *

from get_data_from_db import *

fin_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'mape.csv')
fout=open(fin_path,'w',encoding='UTF-8') #打开文件

def nonintelligent_model(input_data_df=None,config_data_df=None,date_start=None,date_end=None,time2market=None,forecast_model='GBRT',
	evaluation='MAPE',length_merge=1,period=7,required_data_number=5):
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
	# predict_days=28
	# 结果列表
	list_result=[]
	# 所有的对象id
	obj_ids=df['id'].unique() 
	# 循坏每个id
	for index_no,id in enumerate(obj_ids): 
		print('Processing %d-th sku:%s ... There are %d skus in total ...'%(index_no+1,id,len(obj_ids)))
		dict_result=dict()
		dict_result['id']=str(id) # TypeError: Object of type 'int64' is not JSON serializable
		dict_result['model']=forecast_model
		df_tmp=df[df['id']==id] # 将id对应的所有数据取出来
		# 删除类别列
		if 'class' in df.columns:
			df.drop(['class'],axis=1,inplace=True)

		# 删除标签列
		if 'label' in df_tmp.columns:
			df_tmp.drop(['label'],axis=1,inplace=True)

		# (2) 数据填充
		date_min=date_start # 最小日期数据
		date_max=date_end   # 按预测数据来取最大日期
		# 填充缺失日期的数据--训练+测试数据
		df_tmp_config=df_config[(df_config['date']>=date_min) & (df_config['date']<=date_max)]  # 取出holiday和season数据
		df_tmp=pd.merge(df_tmp_config,df_tmp,left_on='date',right_on='date',how='left') # 左连接,所有日期
		df_tmp.fillna({'quantity':0,'promotion':0},inplace=True)     # 将所有缺失的quantity/promotion数据填充为0
		df_tmp=df_tmp.sort_values(by='date')     # 数据填充之前先将数据按时间排序
		df_tmp.fillna(method='ffill',inplace=True)     # 用前置项方式填充其他缺失数据
		# 对上市时间但没有销量时时有用
		df_tmp.fillna(method='bfill',inplace=True)     # 用后置项方式填充其他缺失数据

		# 分割训练和预测数据
		# date_max_train=date_max-7*Day()
		# print('$'*20)
		# print(date_max_train)  #lambda x: 0 if date_min<=x<=date_max_train else 1
		# df_tmp['label']=df_tmp['date'].map(lambda x: 0 if date_min<=x<=date_max_train else 1)
		# print(df_tmp.head(5))
		# print(df_tmp.tail(10))
		y=pd.Series(df_tmp['quantity'].values,index=pd.date_range(date_min,date_max))
		# for date in y.index:
		# 	print(date,y[date])
		y_train=y[:-predict_days]
		y_test=y[-predict_days:]
		
		# (3) 模型训练及滚动预测 integrated_deeplearning_model
		# try:
		# if forecast_model=='CNN':
		# 	y_real,y_fit,y_predict,error_fit=integrated_regression_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
		if forecast_model in regression_methods:
			y_real,y_fit,y_predict,error_fit=integrated_regression_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
		elif forecast_model in timeseries_methods:
			y_real,y_fit,y_predict,error_fit=integrated_timeseries_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
		elif forecast_model in timeseries_exog_methods:
			y_real,y_fit,y_predict,error_fit=integrated_timeseries_exog_model(df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
		elif forecast_model in deeplearning_methods:
			dp_parameters={'HIDDEN_SIZE':55,'NUM_LAYERS':3,'BATCH_SIZE':30,'TRAINING_STEPS':3000}
			y_real,y_fit,y_predict,error_fit=integrated_deeplearning_model(dp_parameters=dp_parameters,df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
		
			# best_RMSE=np.inf
			# for x in range(3,3+1,1):
			# 	for y in range(50,300+1,50):
			# 		dp_parameters={'HIDDEN_SIZE':y,'NUM_LAYERS':x,'BATCH_SIZE':30,'TRAINING_STEPS':3000}
			# 		RMSE_list=[]
			# 		for _ in range(3):
			# 			y_real,y_fit,y_predict,error_fit=integrated_deeplearning_model(dp_parameters=dp_parameters,df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
			# 			RMSE=prediction_RMSE(y_test=array(y_real),y_predict=array(y_fit))
			# 			RMSE_list.append(RMSE)
			# 		RMSE_mean=np.mean(RMSE_list)
			# 		if RMSE_mean<best_RMSE:
			# 			best_RMSE=RMSE_mean
			# 			best_dp_parameters=dp_parameters.copy()
			# y_real,y_fit,y_predict,error_fit=integrated_deeplearning_model(dp_parameters=best_dp_parameters,df=df_tmp,forecast_model=forecast_model,evaluation=evaluation,length_merge=length_merge,period=period)
			# print('&%$*'*20)
			# print(best_dp_parameters)

		else:
			dict_result['code']=1005
			dict_result['desc']="找不到该模型:%s"%forecast_model
			list_result.append(dict_result)
			continue

		# except Exception as e:
		# 	dict_result['error']='模型调用失败(%s)'%(e)
		# 	list_result.append(dict_result)
		# 	continue
		dict_result['y_real']=y_real
		dict_result['y_fit']=y_fit
		dict_result['y_predict']=y_predict
		dict_result[evaluation]=error_fit
		error_pre=evaluation_methods[evaluation](y_test=array(y_test),y_predict=array(y_predict))
		RMSE_final=prediction_RMSE(y_test=array(y_test),y_predict=array(y_predict))
		#############################################
		QQ_y_test=timeseries_merge(y_test,length_merge=7)
		QQ_y_predict=timeseries_merge(y_predict,length_merge=7)
		RMSE=prediction_RMSE(y_test=array(y_test),y_predict=array(y_predict))
		QQ_pre_mape=1-np.abs(array(QQ_y_test)-array(QQ_y_predict))/(array(QQ_y_test)+1)
		dict_result['pre_mape']=list(QQ_pre_mape)
		dict_result['y_test']=list(QQ_y_test)
		dict_result['y_predict']=list(QQ_y_predict)
		new_line=str(id)+','+str(list(QQ_pre_mape))+'\n'
		print(new_line)
		fout.write(new_line)
		##############################################
		integrated_y_test=timeseries_merge(y_test,length_merge=7)
		integrated_y_predict=timeseries_merge(y_predict,length_merge=7)
		integrated_MAPE=prediction_MAPE(y_test=array(integrated_y_test),y_predict=array(integrated_y_predict))
		# 将id的预测结果dict_result添加到结果列表
		# list_result.append(dict_result)
		##################################################################
		fig = plt.figure(id)  
		ax  = fig.add_subplot(111)  
		#解决中文显示问题
		plt.rcParams['font.sans-serif']=['SimHei']
		plt.rcParams['axes.unicode_minus'] = False
		plt.plot(y,'o-',color='purple',label='real_data')
		delete_num=len(y_train)-len(y_fit)
		ts_fit=Series(y_fit,index=y_train.index[delete_num:])
		ts_predict=Series(y_predict,index=y_test.index)
		plt.plot(ts_fit,'o-',color='green',label='fitted_data')
		plt.plot(ts_predict,'o-',color='red',label='predicted_data')
		plt.ylabel("sales volume")
		plt.xlabel('days')
		plt.title("id:%s model:%s\nfitted_MAPE:%.2f predicted_MAPE:%.2f integrated_MAPE:%.2f RMSE:%.2f"%(id,forecast_model,error_fit,error_pre,integrated_MAPE,RMSE_final))
		plt.legend() 
		fig.set_size_inches(16, 8)
		# plt.savefig(forecast_model+'_'+str(id)+'.png',dpi = 300,bbox_inches='tight',pad_inches=None) #,,bbox_inches='tight'
		plt.show()

        #####################################################################

	# 结束循环每个id的预测
	json_result = json.dumps(list_result)
	fout.close()
	return json_result

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

	# 定义上市日期
	time2market="[{'43791':'2018-01-28','41841':'2018-01-28','11111':'2018-01-28'}]"
	time2market = demjson.decode(time2market)[0]
	# 定义开始结束日期
	date_start='2018-01-28'
	date_end='2018-05-02' 
	# date_start='2017-01-01'
	# date_end='2017-12-31' 
	date_start=datetime.datetime.strptime(date_start,'%Y-%m-%d')
	date_end=datetime.datetime.strptime(date_end,'%Y-%m-%d')
	json_result=nonintelligent_model(input_data_df,config_data_df,date_start=date_start,date_end=date_end,time2market=time2market,
			forecast_model='SARIMA',evaluation='MAPE',length_merge=7,period=4)
	text = json.loads(json_result)
	# 打印预测结果
	for x in text:
		print(x)
		# print(x['id'],x['pre_mape'])
