#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-21 12:56:23
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from numpy import *
import pandas as pd
import numpy as np
import copy
from pandas import Series,DataFrame
from pandas.tseries.offsets import Day

'''
该自定义包定义和特征处理相关的函数和变量
'''

# 函数定义
def code_dummies(df):
	'''
	将列的值进行类别编码,再进行独热编码
	将df中所有字符串类型的特征均做热编码
	'''
	# 找出字符串类型的列标
	dummy_cols=[]
	data_types=df.dtypes
	for index in data_types.index:
		if data_types[index]==np.object:
			dummy_cols.append(index)
	# 字符串类型的特征做热编
	for column in dummy_cols:
		values_unique=df[column].unique() # 所有的名称
		value_dict={value:value for index,value in enumerate(values_unique)} #生成编码字典
		df[column]=df[column].map(value_dict) #名称进行类别编码-修改列的值
		value_dummies=pd.get_dummies(df[column],prefix=column)
		df.drop([column],axis=1,inplace=True) # 删除列,直接修改
		df=pd.concat([df,value_dummies],axis=1) # 按列合并
	return df

def normalization(data_X):
	'''
	input:data_X(array)  # array-(n,m)
	output:std_X(array)  # array-(n,m)
	若整列为为唯一值,则标准化后整列均为0
	'''
	#区间缩放,返回值为缩放到[0, 1]区间的数据
	std_X=MinMaxScaler().fit_transform(data_X)
	return std_X

def feature_selection(data_X,data_y,model=DecisionTreeRegressor):
	'''
	input:data_X(array)  # array-(n,m)
		  data_y(list)   # array-(n,)
		  model()   # e.g.,GradientBoostingRegressor,DecisionTreeRegressor
		  		    # GBDT/CART作为基模型的特征选择
	output:selected_features(array) # array-(k,) e.g.,[True False False ...]
	'''
	base_model=model()
	select_model=SelectFromModel(base_model).fit(data_X, data_y)
	selected_features=select_model.get_support() # Get a mask, or integer index, of the features selected
	# print('threshold:',select_model.threshold_)
	return selected_features

def train_test_split_by_reg_random(X,y,test_size=0.2):
	'''
	随机划分训练和测试数据	
	'''
	X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)
	return X_train,X_test,y_train,y_test

def train_test_split_by_reg_order(X,y,test_size=0.2):
	'''
	按顺序划分训练和测试数据
	test_size可以为(0,1)的小数或整数	
	'''
	row_num=len(X) # 行数,即样本数
	if 0<test_size<1:  # 小数
		train_num=int((1-test_size)*row_num)
	else: # 整数
		train_num=row_num-test_size
	X_train,X_test,y_train,y_test=X[:train_num,:],X[train_num:,:],y[:train_num],y[train_num:]
	return X_train,X_test,y_train,y_test

def train_test_split_by_order(timeseries=None,test_size=0.2):
	'''
	按顺序划分训练和测试数据
	test_size可以为(0,1)的小数或整数	
	'''
	row_num=len(timeseries) # 行数,即样本数
	if 0<test_size<1:  # 小数
		train_num=int((1-test_size)*row_num)
	else: # 整数
		train_num=row_num-test_size
	timeseries_train=timeseries[:train_num]
	timeseries_test=timeseries[train_num:]
	return timeseries_train,timeseries_test

def prediction_RMSE(y_test,y_predict):
	'''
	计算测试数据的均方误差
	'''
	return np.sqrt(mean_squared_error(y_test,y_predict))

def prediction_MSE(y_test,y_predict):
	'''
	计算测试数据的均方误差
	'''
	return mean_squared_error(y_test,y_predict)

def prediction_MAE(y_test,y_predict):
	'''
	平均绝对误差
	'''
	return mean_absolute_error(y_test,y_predict)

def prediction_MRE(y_test,y_predict):
	'''
	计算测试数据的预测准确度 a if a>b else b
	The best possible score is 1.0 and it can be negative.
	'''
	# y_test_change=copy.deepcopy(y_test) #注意切不能修改参数的值
	y_test_change=array(y_test)+1
	pre_MRE=np.mean(np.abs((y_test - y_predict) / y_test_change))
	return pre_MRE

# 注:MAPE是越大越好,所以最好不要和其他误差方法放在一起
def prediction_MAPE(y_test,y_predict):
	'''
	计算测试数据的预测准确度 a if a>b else b
	The best possible score is 1.0 and it can be negative.
	'''
	MAPE=1-prediction_MRE(y_test,y_predict)
	return MAPE


def prediction_score(y_test,y_predict):
	'''
	计算测试数据的预测得分
	(1 - u/v),  u:((y_true - y_pred) ** 2).sum() and v:((y_true - y_true.mean()) ** 2).sum(). 
	The best possible score is 1.0 and it can be negative.
	'''
	if len(y_test)==len(y_predict):
		pre_score=1.0-sum((y_test-y_predict)**2)/sum((y_test-mean(y_test))**2) # divide by zero encountered
		return pre_score
	else:
		print("Error:the length of y_test and y_predict are not equal!!!")

def timeseries_merge(timeseries,length_merge=7):
	'''
	timeseries:为一个Series或list类型
	length_merge:为合并的长度
	算法从后往前按length_merge区间长度合并
	输入timeseries,返回也是timeseries;输入list,返回也是list.
	'''
	len_series=len(timeseries)
	quotient,remainder=divmod(len_series,length_merge) # 商数,余数
	label=[] if remainder==0 else [0]
	label_after=array(range(quotient))*length_merge+remainder
	label.extend(label_after); label.append(len_series) # 合并的下标间隔
	arr=[sum(timeseries[label[x]:label[x+1]]) for x in range(len(label)-1)] # 合并
	if isinstance(timeseries, Series):
		index_selected=array(label[1:])-1 # 合并后的索引下标
		new_index=timeseries.index[index_selected] # 合并后的索引
		new_timeseries=Series(arr,index=new_index)
	elif isinstance(timeseries, list):
		new_timeseries=arr
	else:
		new_timeseries=None
	return new_timeseries

def add_lag_feature(df=None,feature_lag={}):
	'''
	feature_lag={'quantity':[1,2,7],'tag_price':[1],'fact_price':[1],'weekend':[1]}
	注:输入df的行必须是按日期升序排列的
	'''
	rows,cols=df.shape
	index=df.index
	for row in range(0,rows):
		for feature in feature_lag:
			for lag in feature_lag[feature]:
				lag_row=row-lag if row-lag>=0 else row
				df.ix[index[row],feature+'_t_'+str(lag)]=df.ix[index[lag_row],feature]
	return df

def ts_append(ts=None,value=0):
	'''
	对于索引为日期的Series添加值 
	'''
	ts_tmp=copy.deepcopy(ts)
	ts_index=ts.index
	days=(ts.index[-1]-ts.index[-2]).days
	index=max(ts.index)+days*Day()
	ts_tmp[index]=value
	return ts_tmp

def X2LSTMX(X=None):
	'''
	对于array X 转化为lstm的输入X 
	'''
	rows,cols=X.shape
	lstm_X=[]
	for row in range(rows):
		lstm_X.append([list(X[row])])
	return np.array(lstm_X, dtype=np.float32)

def con_LSTM(y_series=None,zero_num=7): # 计算时间序列的差分d值
	# 检查非零数据的数量是否>=10
	non_zeros=sum(np.array(y_series)>0)
	if non_zeros>=10:
		data_amount_check=True
	else:
		data_amount_check=False
	# 检查是否存在2次连续至少zero_num个为0的数据
	intermittent=0
	k=0
	end_k=len(y_series)-zero_num
	while True: 
		if k<=end_k:
			if y_series[k]==0:
				if sum(y_series[k:k+zero_num])==0:
					intermittent=intermittent+1
					k=k+zero_num
					while True:
						if k<=end_k and y_series[k]==0:
							k=k+1
						else:
							break
				else:
					k=k+1
			else:
				k=k+1
		else:
			break
	if data_amount_check and intermittent>=2:
		return True
	else:
		return False


def con_ARIMA(y_series=None): # 计算时间序列的差分d值
	'''
	时间序列平稳性检验,p-value<0.05则通过,否则不通过
	最大差分次数max_diff_time=2
	注意:可能1次差分可通过白噪声检验,但2次差分通不过
	'''
	# 检查数据量是否>=50
	if len(y_series)>=50:
		data_amount_check=True
	else:
		data_amount_check=False
	# 检查是否可2阶内差分平稳
	df_obj=pd.DataFrame(y_series) # 将Series(name=quantity)转化为DataFrame
	df_obj['week_num']=df_obj.index.map(lambda x: x.weekday())
	y_df=df_obj[['quantity','week_num']]
	y_avg=y_df.groupby('week_num').quantity.aggregate([np.mean])
	y_avg=y_avg.ix[:,0]
	df_obj['week_num']=df_obj['week_num'].map(lambda x: y_avg[x])
	y_series_sub=df_obj['quantity']-df_obj['week_num']
	ts_diff=y_series_sub.copy()

	isStationarity=False
	p_value_shreshold = 0.05
	d=0
	max_diff_time = 2
	while True:
		# 白噪声检验结果
		lbvalue,pvalue2=acorr_ljungbox(ts_diff,lags=1) 
		rule_1=(pvalue2<p_value_shreshold)
		# ADF检验,平稳性检验
		adf,pvalue1,usedlag,nobs,critical_values,icbest= adfuller(ts_diff) 
		rule_2=(adf<critical_values['1%'] and adf<critical_values['5%'] and adf<critical_values['10%'] and pvalue1<0.01) 
		# 忽略白噪声检验 rule_1 and
		if rule_1 and rule_2:
			isStationarity=True
			break
		if not (rule_1 and rule_2) and d < max_diff_time:
			d = d + 1
			ts_diff = y_series_sub.diff(d) #进行d阶差分
			ts_diff.dropna(inplace=True) #丢掉缺失值,If True, do operation inplace and return None.
		else:
			break
	return data_amount_check and isStationarity


def con_SARIMAX(y_series=None,season=7): 
	'''
	时间序列平稳性检验,p-value<0.05则通过,否则不通过
	最大差分次数max_diff_time=2
	'''
	# 检查数据量是否>=50
	if len(y_series)>=50:
		data_amount_check=True
	else:
		data_amount_check=False
	# 检查1阶差分+周期差分是否可平稳
	isStationarity=False
	p_value_shreshold = 0.05
	# 1阶差分
	ts_diff = y_series.diff(1) # 不会改变y_series的值
	ts_diff.dropna(inplace=True) # 丢掉缺失值,If True, do operation inplace and return None.
	#进行周期差分
	ts_diff = y_series.diff(season) 
	ts_diff.dropna(inplace=True) #丢掉缺失值,If True, do operation inplace and return None.
	# 白噪声检验结果
	lbvalue,pvalue2=acorr_ljungbox(ts_diff,lags=1) 
	rule_1=(pvalue2<p_value_shreshold)
	# ADF检验,平稳性检验
	adf,pvalue1,usedlag,nobs,critical_values,icbest= adfuller(ts_diff) 
	rule_2=(adf<critical_values['1%'] and adf<critical_values['5%'] and adf<critical_values['10%'] and pvalue1<0.01) 
	# 忽略白噪声检验 rule_1 and
	if rule_2:
		isStationarity=True

	return data_amount_check and isStationarity


# 变量定义
evaluation_methods={'MSE':prediction_MSE,'RMSE':prediction_RMSE,'MAE':prediction_MAE,'MRE':prediction_MRE,'MAPE':prediction_MAPE}


#测试代码
if __name__=='__main__':
	pass
	from get_data_from_db import *
	print(input_data_df.head(10))
	date_min=min(input_data_df['date'])
	date_max=max(input_data_df['date'])
	df_train_test=input_data_df[['date','quantity']] # 选取日期和销量列
	df_train_test=df_train_test.set_index(['date']) # 将date列设置为索引,仍然为DataFrame
	train_test_dates=pd.date_range(date_min,date_max) # 有效的历史日期
	df_train_test=df_train_test.reindex(train_test_dates,fill_value=0) # 重新索引 
	df_train_test=df_train_test.astype(np.float64) # 将其转化为float64 ******
	y=df_train_test['quantity']
	res=con_ARIMA(y)
	print(res)
	res1=con_SARIMAX(y)
	print(res1)
	# y_test=[0.0, 1.0, 0.0, 0.0, 0.0]
	# y_predict=[0.0, 0.0, 0.0, 2.0, 0.0]
	# print(y_test)
	# print(y_predict)
	# pre_MRE=prediction_MRE(y_test=array(y_test),y_predict=array(y_predict))
	# pre_MAPE=prediction_MAPE(array(y_test),array(y_predict))
	# print(pre_MRE,pre_MAPE)

	# num=19
	# ts=Series(np.random.randint(10,size=num),index=pd.date_range('1/1/2018',periods=num,freq='d'))
	# print(timeseries_merge(ts,length_merge=5))

	# df=DataFrame(np.arange(12.).reshape((4,3)),columns=list('abc'),index=['kang','guo','sheng','haha'])
	# print(df)
	# df.ix['kang','b']=np.NaN
	# df.ix['haha','b']=np.NaN
	# print(df)
	# df.fillna(method='ffill',inplace=True)     # 用前置项方式填充其他缺失数据
	# print(df)
	# df.fillna(method='bfill',inplace=True) 
	# print(df)

	# tmp_df=normalization(df)
	# df=DataFrame(tmp_df,columns=df.columns,index=df.index)
	# print(df)

	# a=[0,0,0,0,0,0,3,4,5,5,0,0,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,4,4,3,0,0,0,0,0]
	# print(a)
	# print(con_LSTM(a))
