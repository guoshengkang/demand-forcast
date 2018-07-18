#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 18:03:21
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import json
import demjson
from pandas.tseries.offsets import Day
# from matplotlib import pyplot as plt
# 导入自定义的包
from feature_engineering import *
from deeplearning_models import *

'''
#变量deeplearning_methods来自自定义包:deeplearning_models
deeplearning_methods={'LSTM':dp_LSTM}
#变量evaluation_methods来自自定义包:feature_engineering
evaluation_methods={'MSE':prediction_MSE,'RMSE':prediction_RMSE,'MAE':prediction_MAE,'MAPE':prediction_MAPE}
'''

def integrated_deeplearning_model(dp_parameters=dict(),df=None,forcast_model='LSTM',evaluation='MAPE',length_merge=2,period=5):
	'''
	深度学习的预测方法
	--input parameters--
	df:预测的输入数据--DataFrame(训练+预测)
	forcast_model:预测模型
	evaluation:预测评估方法
	length_merge:数据合并的天数
	period:预测的周期
	'''
	df_tmp=df.copy()
	predict_days=length_merge*period

	# (1) 数据预处理
	df_tmp['week_num']=df_tmp['date'].map(lambda x: x.weekday())
	index_train=df_tmp.index[:-predict_days]
	# 在训练集中求按星期的销量平均
	df_mean=df_tmp.ix[index_train,['quantity','week_num']]
	y_avg=df_mean.groupby('week_num').quantity.aggregate([np.mean]) # 返回DataFrame
	y_avg=y_avg.ix[:,0] # 取第1列,等价于y_avg['mean'],返回Series
	# 将week_num列的值映射为按星期的平均销量
	df_tmp['week_num']=df_tmp['week_num'].map(lambda x: y_avg[x])  
	# 增加t-1,t-2,t-7的特征
	feature_lag={'quantity':[1,2,7],'tag_price':[1],'fact_price':[1],'weekend':[1]}
	df_tmp=add_lag_feature(df=df_tmp,feature_lag=feature_lag)
	# 保留y的原始值Series和平均值Series
	df_tmp=df_tmp.set_index(['date'])   # 将date列设置为索引,仍然为DataFrame
	y_series_mean=df_tmp['week_num']     # y的平均值Series
	y_series_original=df_tmp['quantity'] # y的原始值Series
	# 删除列,直接修改
	df_tmp.drop(['quantity','week_num'],axis=1,inplace=True) 
	# 特征独热编码,将所有字符串类型的特征均做热编码
	df_tmp=code_dummies(df_tmp)
	# 取出输入数据X
	X=df_tmp.values.astype(np.float32) 
	# 数据的标准化
	X=normalization(data_X=X)
	# 将标准化的数据加上表头,转化为DataFrame
	X_df=pd.DataFrame(X,index=df_tmp.index,columns=df_tmp.columns)
	
	# (2) 模型训练及滚动预测
	y_copy=y_series_original.copy()
	y_max=max(y_copy[:-predict_days])
	y_min=min(y_copy[:-predict_days])
	y_series_sub=y_series_original-y_series_mean
	# 输入数据的特征列表
	features=X_df.columns
	# 取出训练数据df
	X_df_train=X_df[:-predict_days].copy()
	X=X_df_train.values.astype(np.float32) 
	y_train=y_series_sub[:-predict_days].astype(np.float32) 
	# 取出预测数据df    
	X_df_test=X_df[-predict_days:].copy() # else-->A value is trying to be set on a copy of a slice from a DataFrame
	# 定义预测结果列表
	prediction_y=[]
	# 迭代预测每一个预测样本
	for k,index in enumerate(X_df_test.index):
		t_1=index-1*Day()
		t_2=index-2*Day()
		t_7=index-7*Day()
		X_df_test.ix[index,'quantity_t_1']=(y_copy[t_1]-y_min)/(y_max-y_min)
		X_df_test.ix[index,'quantity_t_2']=(y_copy[t_2]-y_min)/(y_max-y_min)
		X_df_test.ix[index,'quantity_t_7']=(y_copy[t_7]-y_min)/(y_max-y_min)
		# 特征选取
		if k==0: # 特征选取,只做一次
			selected_features=feature_selection(data_X=X,data_y=y_train)
			final_features=list(np.array(features)[selected_features])
			X_train=X_df_train.ix[:,selected_features].values # 特征选择之后的X
			X_train=X2LSTMX(X_train) # 转化为LSTM模型的输入X
		X_test=X_df_test.ix[index,final_features].values.astype(np.float32)  # 取一行的话,结果是向量
		X_test=np.array(X_test).reshape(1,len(X_test))
		X_test=X2LSTMX(X_test) # 转化为LSTM模型的输入X
		# 模型训练
		if k==0: # 模型训练,只做一次
			# 模型初始化
			model=deeplearning_methods[forcast_model](**dp_parameters)
			# 模型训练
			model.fit(X_train,y_train)
		predicted=model.predict(X_test)+array(y_series_mean[index]) # 预测一个值
		y_copy[index]=predicted[0]
	# 预测数据
	y_predict=y_copy[-predict_days:]
	# 拟合数据
	y_fit=model.predict(X_train)+array(y_series_mean[:-predict_days])
	# 真实数据
	y_real=y_series_original[:-predict_days]
	# 计算训练数据的拟合误差
	error_fit=evaluation_methods[evaluation](y_test=array(y_real),y_predict=array(y_fit))
	# 四舍五入保留2位小数
	y_real=list(np.round(y_real,2))
	y_fit=list(np.round(y_fit,2))
	y_predict=list(np.round(y_predict,2))
	error_fit=np.round(error_fit,2) 

	return y_real,y_fit,y_predict,error_fit
