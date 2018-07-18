#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-28 12:19:18
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import itertools
import numpy as np
from numpy import *
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pylab as plt
import statsmodels.tsa.stattools as st
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
from pyramid.arima import auto_arima

# 导入自定义的包
from feature_engineering import *
'''
该自定义包定义和时间序列模型相关的类和变量
'''

# 类定义---------------------------------------------------
# AR Model
# Ref:https://blog.csdn.net/matrix_laboratory/article/details/53912312
class ts_AR:
	"""
	Parameters
	------------
	ts_train:训练数据
	error_fun:使用的误差函数
	Attributes
	------------
	fittedModel:拟合的模型
	"""
	def __init__(self,ts_train,error_fun=None):
		self.ts_train = ts_train # 训练时间序列
		self.error_fun = error_fun
		self.fittedModel = None

	def __adf_test(self):
	    adftest = adfuller(self.ts_train, autolag='AIC')
	    # 'Test Statistic','p-value','Lags Used','Number of Observations Used',XX
		# (-0.0, 0.958532086060056, 9, 10, {'1%': -4.331573, '5%': -3.23295, '10%': -2.7487}, -582.412544847778)
	    adf_res = pd.Series(adftest[0:4], index=['Test Statistic','p-value','Lags Used','Number of Observations Used'])
	    for key, value in adftest[4].items():
	        adf_res['Critical Value (%s)' % key] = value
	    return adf_res

	def fit(self):
		adf_res=self.__adf_test()
		w=int(adf_res['Lags Used'])
		self.fittedModel = ARMA(self.ts_train, order=(w, 0)).fit(disp = -1)

	def get_fittedvalues(self): #预测拟合值
		fittedvalues = self.fittedModel.predict() # 等价于self.fittedModel.fittedvalues Series类型
		fittedvalues=np.round(fittedvalues) # 将预测的销量四舍五入
		return fittedvalues #array类型

	def predict(self,forcast_period=2):
		y_forcast = self.fittedModel.forecast(forcast_period)[0] 
		y_forcast=np.round(y_forcast) # 将预测的销量四舍五入
		return y_forcast


# MA Model
# Ref:https://blog.csdn.net/matrix_laboratory/article/details/53942888
class ts_MA:
	"""
	Parameters
	------------
	ts_train:训练数据
	error_fun:使用的误差函数
	Attributes
	------------
	fittedModel:拟合的模型
	"""
	def __init__(self,ts_train,error_fun=None):
		self.ts_train = ts_train # 训练时间序列
		self.error_fun = error_fun
		self.fittedModel = None

	def __adf_test(self):
	    adftest = adfuller(self.ts_train, autolag='AIC')
	    # 'Test Statistic','p-value','Lags Used','Number of Observations Used',XX
		# (-0.0, 0.958532086060056, 9, 10, {'1%': -4.331573, '5%': -3.23295, '10%': -2.7487}, -582.412544847778)
	    adf_res = pd.Series(adftest[0:4], index=['Test Statistic','p-value','Lags Used','Number of Observations Used'])
	    for key, value in adftest[4].items():
	        adf_res['Critical Value (%s)' % key] = value
	    return adf_res

	def fit(self):
		adf_res=self.__adf_test()
		w=int(adf_res['Lags Used'])
		self.fittedModel = ARMA(self.ts_train, order=(0, w)).fit(disp = -1)

	def get_fittedvalues(self): #预测拟合值
		fittedvalues = self.fittedModel.predict() # 等价于self.fittedModel.fittedvalues Series类型
		fittedvalues=np.round(fittedvalues) # 将预测的销量四舍五入
		return fittedvalues #array类型

	def predict(self,forcast_period=2):
		y_forcast = self.fittedModel.forecast(forcast_period)[0] 
		y_forcast=np.round(y_forcast) # 将预测的销量四舍五入
		return y_forcast


# ARMA Model
class ts_ARMA(object):
	"""
	Parameters
	------------
	ts_train:训练数据
	error_fun:使用的误差函数

	Attributes
	------------
	max_ar:p的最大取值
	max_ma:q的最大取值
	fittedModel:拟合的模型
	"""
	def __init__(self,ts_train,error_fun=None):
		#统计量的P值小于显著性水平0.05，则可以以95%的置信水平拒绝原假设，
		#认为序列为非白噪声序列(否则，接受原假设，认为序列为纯随机序列)
		self.ts_train = ts_train
		self.error_fun = error_fun
		self.max_ar = 6
		self.max_ma = 4 
		self.max_log = 5
		self.best_log = 0
		self.p_value_shreshold = 0.05 # 平稳性检测p_value值
		self.p = 0
		self.q = 0
		self.fittedModel = None
		self.bic = inf

	def get_best_log(self,ts,rule1=True,rule2=True):
		if rule1 and rule2:
			return ts
		else:
			for i in range(1,self.max_log):
				ts=np.log(ts+1) #存在0的情况,会导致检验程序进入死循环
				lbvalue,pvalue2=acorr_ljungbox(ts,lags=1) #白噪声检验结果
				adf,pvalue1,usedlag,nobs,critical_values,icbest= adfuller(ts) #ADF检验
				rule_1=(adf<critical_values['1%'] and adf<critical_values['5%'] and adf<critical_values['10%'] and pvalue1<0.01) 
				rule_2=(pvalue2<self.p_value_shreshold)
				rule_3=(i<self.max_log)
				self.best_log=i
				if rule_1 and rule_2 and rule_3:
					print('The best log n is:{0}'.format(i))
					break
		return ts

	def recover_log(self,ts):
		for _ in range(1,self.best_log+1):
			ts=np.exp(ts)-1
		return ts

	def fit(self):
		lbvalue,pvalue2=acorr_ljungbox(self.ts_train,lags=1) #白噪声检验结果
		adf,pvalue1,usedlag,nobs,critical_values,icbest= adfuller(self.ts_train) #ADF检验
		rule_1=(adf<critical_values['1%'] and adf<critical_values['5%'] and adf<critical_values['10%'] and pvalue1<0.01) 
		rule_2=(pvalue2<self.p_value_shreshold)
		ts=self.get_best_log(ts=self.ts_train,rule1=rule_1,rule2=rule_2)
		for p in np.arange(self.max_ar+1):
			for q in np.arange(self.max_ma+1):
				# print('p={0},q={1}'.format(p,q))
				model = ARMA(ts, order=(p,q)) #使用差分后的数据进行Arima模型的训练
				try:
					results_ARMA = model.fit(disp=-1, method='css')
				except:
					continue
				bic = results_ARMA.bic
				if bic < self.bic:
					self.p = p
					self.q = q
					self.fittedModel = results_ARMA
					self.bic = bic

	def get_fittedvalues(self): #预测拟合值
		fittedvalues = self.fittedModel.predict() # 等价于self.fittedModel.fittedvalues Series类型
		# fittedvalues=np.round(fittedvalues) # 将预测的销量四舍五入
		return self.recover_log(fittedvalues) #array类型

	def predict(self,forcast_period=2):
		y_forcast = self.fittedModel.forecast(forcast_period)[0] 
		return self.recover_log(y_forcast)


# ARIMA Model
# Ref:https://www.cnblogs.com/bradleon/p/6827109.html
# Ref:https://blog.csdn.net/u010414589/article/details/49622625
class ts_ARIMA(object):
	"""
	Parameters
	------------
	ts_train:训练数据
	error_fun:使用的误差函数

	Attributes
	------------
	max_ar:p的最大取值
	max_ma:q的最大取值
	max_diff_time:最大差分次数,将影响预测数据的还原函数:predict_recover
	p_value_shreshold:平稳性检验的P值阈值
	fittedModel:拟合的模型
	diffs:保留的每次差分结果
	ts_diff:最终的差分结果
	"""

	def __init__(self,ts_train,error_fun=None):
		#统计量的P值小于显著性水平0.05，则可以以95%的置信水平拒绝原假设，
		#认为序列为非白噪声序列(否则，接受原假设，认为序列为纯随机序列)
		self.ts_train = ts_train
		self.error_fun = error_fun
		self.max_ar = 15
		self.max_ma = 15 
		self.order = None
		self.seasonal_order=(0,0,0,0)
		self.max_diff_time = 2 
		self.p_value_shreshold = 0.05 # 平稳性检测p_value值
		self.fittedModel = None
		self.predict_ts = None # Series 训练数据的预测值
		self.d = 0
		self.bic = np.inf
		self.diffs=[ts_train]
		self.ts_diff = ts_train
		self.isStationarity=False
		

	# private私有函数
	def __ts_differencing(self): # 计算时间序列的差分d值
		'''
		时间序列平稳性检验,p-value<0.05则通过,否则不通过
		最大差分次数max_diff_time=2 
		'''
		while True:
			lbvalue,pvalue2=acorr_ljungbox(self.ts_diff,lags=1) #白噪声检验结果
			adf,pvalue1,usedlag,nobs,critical_values,icbest= adfuller(self.ts_diff) #ADF检验
			rule_1=(adf<critical_values['1%'] and adf<critical_values['5%'] and adf<critical_values['10%'] and pvalue1<0.01) 
			rule_2=(pvalue2<self.p_value_shreshold)
			if rule_1 and rule_2:
				self.isStationarity=True
				break
			if not (rule_1 and rule_2) and self.d < self.max_diff_time:
				self.d = self.d + 1
				self.ts_diff = self.ts_train.diff(self.d) #进行d阶差分
				self.diffs.append(self.ts_diff)
				self.ts_diff.dropna(inplace=True) #丢掉缺失值,If True, do operation inplace and return None.
			else:
				break

	def __predict_recover(self,y_predict):
		'''
		根据差分,还原预测数据
		d=0: Y(t)=y(t)
		d=1: Y(t)=y(t)+Y(t-1)
		d=2: Y(t)=y(t)+2*Y(t-1)-Y(t-2)
		'''
		tmp_ts=Series(np.zeros(len(y_predict)),index=y_predict.index)
		if self.d==1:
			for t in tmp_ts.index:
				tmp_ts[t]=y_predict[t]+self.ts_train[t-1]
		elif self.d==2:
			for t in tmp_ts.index:
				tmp_ts[t]=y_predict[t]+2*self.ts_train[t-1]-self.ts_train[t-2]
		else: #
			pass
		return tmp_ts

	def fit(self): #训练模型
		self.__ts_differencing()
		# order = st.arma_order_select_ic(self.ts_diff,max_ar=self.max_ar,max_ma=self.max_ma,ic=['aic', 'bic', 'hqic'])
		# self.p,self.q=order.bic_min_order #速度慢,所以不建议使用,但是求得结果不一样
		for p in np.arange(self.max_ar+1):
			for q in np.arange(self.max_ma+1):
				model = ARIMA(self.ts_train, order=(p,self.d,q)) #使用差分后的数据进行Arima模型的训练
				try:
					results_ARIMA = model.fit(disp=-1, method='css')
				except:
					continue
				bic = results_ARIMA.bic
				if bic < self.bic:
					self.order=(p,self.d,q)
					self.fittedModel = results_ARIMA
					self.bic = bic

	def get_fittedvalues(self): #预测拟合值
		fittedvalues = self.fittedModel.predict() # 等价于self.fittedModel.fittedvalues Series类型
		if self.d>0:
			fittedvalues = self.__predict_recover(fittedvalues) # Series类型
		return fittedvalues #array类型

	def predict(self,forcast_period=2):
		y_forcast = self.fittedModel.forecast(forcast_period)[0] 
		return y_forcast  # 返回array

	# 滚动预测方式,效果相差很小,暂不采用
	def rolling_predict(self,forcast_period=2):
		ts_tmp=self.ts_train.copy()
		model_tmp=self.fittedModel
		y_forcast=[]
		for _ in range(forcast_period):
			yhat = model_tmp.forecast()[0][0]
			y_forcast.append(yhat)
			ts_tmp=ts_append(ts=ts_tmp,value=yhat)
			rolling_model = ARIMA(ts_tmp, order=(self.p,self.d,self.q))
			model_tmp = rolling_model.fit(disp=-1, method='css')
		print()
		return array(y_forcast)  # 返回array

# SARIMAX
# Ref: http://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html
# Ref: https://blog.csdn.net/u014096903/article/details/79980036
# Ref: https://www.digitalocean.com/community/tutorials/a-guide-to-time-series-forecasting-with-arima-in-python-3
class ts_SARIMAX(object):
	def __init__(self,ts_train,error_fun=None):
		self.ts_train = ts_train
		self.error_fun = error_fun
		self.bic = np.inf
		self.fittedModel = None
		self.order=None
		self.seasonal_order=None

	def fit(self): #训练模型
		# d = range(0, 3)
		# p = q = range(0, 6)
		# pdq = list(itertools.product(p, d, q))
		P = D = Q = range(0, 2)
		PDQ = list(itertools.product(P, D, Q))
		seasonal_pdq = [(x[0], x[1], x[2], 7) for x in PDQ]
		for param in PDQ:
			for param_seasonal in seasonal_pdq:
				try:
					model = sm.tsa.statespace.SARIMAX(self.ts_train,
						order=param,
			            seasonal_order=param_seasonal,
			            enforce_stationarity=False,
			            enforce_invertibility=False)
					results_SARIMAX = model.fit(disp=False)
				except:
					continue
				bic = results_SARIMAX.bic
				if bic < self.bic:
					self.fittedModel = results_SARIMAX
					self.bic = bic
					self.order=param
					self.seasonal_order=param_seasonal

	def get_fittedvalues(self): #预测拟合值
		fittedvalues=self.fittedModel.predict()
		return fittedvalues #array类型

	def predict(self,forcast_period=2):
		y_forcast = self.fittedModel.forecast(steps=forcast_period)  # 返回Series
		return y_forcast  # 返回array


# https://zhuanlan.zhihu.com/p/39533849
class ts_AUTO_ARIMA(object):
	def __init__(self,ts_train,error_fun=None):
		self.ts_train = ts_train
		self.error_fun = error_fun
		self.start_p = 0
		self.d = None
		self.start_q=0
		self.max_p=15
		self.max_d=5
		self.max_q=15
		self.max_order=None
		self.m=7
		self.seasonal=True
		self.stationary=False
		self.stepwise=False
		self.fittedModel = None
		# (p,d,q)=fittedModel.order
		# (P,D,Q,s)=fittedModel.seasonal_order
	def fit(self): #训练模型
		# self.fittedModel = auto_arima(y=self.ts_train)
		self.fittedModel = auto_arima(y=self.ts_train, 
			start_p=self.start_p, 
			start_q=self.start_q, 
			max_p=self.max_p, 
			max_q=self.max_q, 
			max_d=self.max_d,
			max_order=self.max_order,
			seasonal=self.seasonal,
			m=self.m, 
			# start_P=2,
			# start_Q=0,
			# D=1,
			# max_Q=0,
			maxiter=1000,
			test='adf', 
			trace=False,           
			error_action='ignore',  # don't want to know if an order does not work
			suppress_warnings=True,  # don't want convergence warnings
			stepwise=self.stepwise, 
			information_criterion='bic', 
			njob=-1)

	def get_fittedvalues(self): #预测拟合值
		fittedvalues=self.fittedModel.predict_in_sample()
		return fittedvalues #array类型

	def predict(self,forcast_period=2):
		y_forcast = self.fittedModel.predict(forcast_period) # 返回array
		return y_forcast  # 返回array

	# 滚动预测方式,效果相差很小,暂不采用
	# def predict(self,forcast_period=2):
	# 	ts_tmp=self.ts_train.copy()
	# 	model_tmp=self.fittedModel
	# 	y_forcast=[]
	# 	for _ in range(forcast_period):
	# 		yhat = model_tmp.predict(1)[0]
	# 		y_forcast.append(yhat)
	# 		ts_tmp=ts_append(ts=ts_tmp,value=yhat)
	# 		model_tmp= auto_arima(y=self.ts_train, 
	# 		start_p=self.start_p, 
	# 		start_q=self.start_q, 
	# 		max_p=self.max_p, 
	# 		max_q=self.max_q, 
	# 		max_d=self.max_d,
	# 		max_order=self.max_order,
	# 		seasonal=self.seasonal,
	# 		m=self.m, 
	# 		test='adf', 
	# 		trace=False,           
	# 		error_action='ignore',  # don't want to know if an order does not work
	# 		suppress_warnings=True,  # don't want convergence warnings
	# 		stepwise=self.stepwise, 
	# 		information_criterion='bic', 
	# 		njob=-1)
	# 	return array(y_forcast)  # 返回array


# Simple Moving Average Model
class ts_SMA:
	"""
	Parameters
	------------
	ts_train:训练数据
	error_fun:使用的误差函数
	Attributes
	------------
	fittedModel:移动窗口
	注:该方法无论多少数据均能预测
	移动窗口<=len(ts_train)-1
	其中,len(ts_train)=1 or 2时,移动窗口=1
	"""
	def __init__(self,ts_train,error_fun=None):
		self.ts_train = ts_train # 时间序列
		self.error_fun = error_fun
		self.min_window=3
		self.max_window=5
		self.best_window=self.max_window

	def fit(self):
		if len(self.ts_train)==1:
			self.best_window=1
		elif 1<len(self.ts_train)<=5:
			self.best_window=len(self.ts_train)-1
		else:
			min_error=inf
			y_train=list(self.ts_train) #转化为list
			for window in range(self.min_window,self.max_window+1):
				fit_list=[]
				for k in range(window, len(y_train)):
					tmp_list = y_train[(k-window):k]
					fit_list.append(mean(tmp_list))
				fittedvalues=fit_list
				error=self.error_fun(y_test=array(y_train[window:]),y_predict=fittedvalues)
				if error<min_error:
					min_error=error
					self.best_window=window

	def get_fittedvalues(self): #预测拟合值
		if len(self.ts_train)==1:
			fittedvalues=array(ts)
		else:
			y_train=list(self.ts_train) #转化为list
			fit_list=[]
			for k in range(self.best_window, len(y_train)):
				tmp_list = y_train[(k-self.best_window):k]
				fit_list.append(mean(tmp_list))
			fittedvalues=fit_list 
		return fittedvalues #array类型

	def predict(self,forcast_period=2):
		if len(self.ts_train)==1:
			y_forcast=array([self.ts_train[0]]*forcast_period)
		else:
			list_tmp=list(self.ts_train) #转化为list
			for _ in range(forcast_period):
				list_len=len(list_tmp)
				start=max(list_len-self.best_window,0)
				predict_value=np.mean(list_tmp[start:list_len])
				list_tmp.append(predict_value)
			y_forcast=list_tmp[-forcast_period:]
		return y_forcast

# Weighted Moving Average Model
class ts_WMA:
	"""
	Parameters
	------------
	ts_train:训练数据
	error_fun:使用的误差函数
	Attributes
	------------
	fittedModel:移动窗口
	注:该方法无论多少数据均能预测
	len(ts_train)<=5时,移动窗口=len(ts_train)-1
	其中,len(ts_train)=1时,移动窗口=1
	"""
	def __init__(self,ts_train,error_fun=None):
		self.ts_train = ts_train # 时间序列
		self.error_fun = error_fun
		self.min_window=3
		self.max_window=5
		self.best_window=self.max_window
		self.best_weights=None

	def fit(self):
		if len(self.ts_train)==1:
			self.best_window=1
			self.best_weights=[1.0]
		elif 1<len(self.ts_train)<=5:
			self.best_window=len(self.ts_train)-1
			numbers=array(range(1,len(self.ts_train)))
			self.best_weights=numbers/sum(numbers) #加权平均的权重
		else:
			min_error=inf
			y_train=list(self.ts_train) #转化为list
			for window in range(self.min_window,self.max_window+1):
				numbers=array(range(1,window+1))
				weights=numbers/sum(numbers) #加权平均的权重
				fit_list=[]
				for k in range(window, len(y_train)):
					tmp_list = y_train[(k-window):k]
					fit_list.append(sum(tmp_list*weights))
				fittedvalues=fit_list
				error=self.error_fun(y_test=array(y_train[window:]),y_predict=fittedvalues)
				if error<min_error:
					min_error=error
					self.best_window=window
					self.best_weights=weights

	def get_fittedvalues(self): #预测拟合值
		if len(self.ts_train)==1:
			fittedvalues=array(ts)
		else:
			y_train=list(self.ts_train) #转化为list
			fit_list=[]
			for k in range(self.best_window, len(y_train)):
				tmp_list = y_train[(k-self.best_window):k]
				fit_list.append(sum(tmp_list*self.best_weights))
			fittedvalues=fit_list
		return fittedvalues #array类型

	def predict(self,forcast_period=2):
		if len(self.ts_train)==1:
			y_forcast=array([self.ts_train[0]]*forcast_period)
		else:
			list_tmp=list(self.ts_train) #转化为list
			for _ in range(forcast_period):
				list_len=len(list_tmp)
				start=max(list_len-self.best_window,0)
				predict_value=sum(list_tmp[start:list_len]*self.best_weights)
				list_tmp.append(predict_value)
			y_forcast=list_tmp[-forcast_period:]
		return y_forcast

# Exponential Smoothing Model 二次
# Ref:https://www.cnblogs.com/TTyb/p/5716125.html
# Ref:https://blog.csdn.net/alanconstantinelau/article/details/70173561
class ts_ES2:
	"""
	Parameters
	------------
	ts_train:训练数据
	error_fun:使用的误差函数
	Attributes
	------------
	best_alpha:训练过程中预测误差最小时的alpha值
	best_error:训练时的预测周期最小误差
	a:模型y=a+b*t的参数
	b:模型y=a+b*t的参数
	fittedvalues:历史数据的拟合值
	es_time=指数平滑次数
	"""
	def __init__(self,ts_train,error_fun=None):
		self.ts_train  = ts_train # 时间序列
		self.error_fun = error_fun
		self.best_alpha=None
		self.best_error=inf
		self.a=None
		self.b=None
		self.fittedvalues=None # array
		self.es_time=2

	def _es1(self,X=[],alpha=0.8): # 1次指数平滑
		S1=[]
		S1.append(X[0]) #S1[0]=X[0]
		for t in range(1,len(X)):
			St=alpha*X[t]+(1-alpha)*S1[t-1]
			S1.append(St)
		return S1

	def _esn(self,X=[],alpha=0.8): # es_time次指数平滑
		S0=X
		esn_dict=dict()
		esn_dict[0]=S0
		for time in range(self.es_time): 
			S1=self._es1(S0,alpha)
			S0=S1
			esn_dict[time+1]=S0
		return esn_dict

	def fit(self):
		X=list(self.ts_train)
		# 重新训练模型参数,寻找最优的alpha值
		for alpha in arange(0.1,1,0.1): # 0.1~0.9
			esn_dict=self._esn(X=X,alpha=alpha)
			S1=esn_dict[1]; S2=esn_dict[2]
			S1t=S1[-1]; S2t=S2[-1]
			a=2*S1t-S2t 
			b=(alpha/(1-alpha))*(S1t-S2t)
			fittedvalues=np.round(S2) # 将预测的销量四舍五入
			error=self.error_fun(y_test=array(X),y_predict=fittedvalues)
			if error<self.best_error:
				self.best_error=error
				self.best_alpha=alpha
				self.a=a
				self.b=b
				self.fittedvalues=fittedvalues

	def get_fittedvalues(self):   # 预测拟合值
		return self.fittedvalues  # array

	def predict(self,forcast_period=2):
		t=arange(1,forcast_period+1)
		y_predict= self.a+self.b*t
		return np.round(y_predict) # array

# Exponential Smoothing Model 三次
# Ref:https://www.cnblogs.com/TTyb/p/5716125.html
# Ref:https://blog.csdn.net/alanconstantinelau/article/details/70173561
class ts_ES3:
	"""
	Parameters
	------------
	ts_train:训练数据
	error_fun:使用的误差函数
	Attributes
	------------
	best_alpha:训练过程中预测误差最小时的alpha值
	best_error:训练时的预测周期最小误差
	a:模型y=a+b*t+c*t^2的参数
	b:模型y=a+b*t+c*t^2的参数
	fittedvalues:历史数据的拟合值
	es_time=指数平滑次数
	"""
	def __init__(self,ts_train,error_fun=None):
		self.ts_train  = ts_train # 时间序列
		self.error_fun = error_fun
		self.best_alpha=None
		self.best_error=inf
		self.a=None
		self.b=None
		self.fittedvalues=None # array
		self.es_time=3

	def _es1(self,X=[],alpha=0.8): # 1次指数平滑
		S1=[]
		S1.append(X[0]) #S1[0]=X[0]
		for t in range(1,len(X)):
			St=alpha*X[t]+(1-alpha)*S1[t-1]
			S1.append(St)
		return S1

	def _esn(self,X=[],alpha=0.8): # es_time次指数平滑
		S0=X
		esn_dict=dict()
		esn_dict[0]=S0
		for time in range(self.es_time): 
			S1=self._es1(S0,alpha)
			S0=S1
			esn_dict[time+1]=S0
		return esn_dict

	def fit(self):
		X=list(self.ts_train)
		# 重新训练模型参数,寻找最优的alpha值
		for alpha in arange(0.1,1,0.1): # 0.1~0.9
			esn_dict=self._esn(X=X,alpha=alpha)
			S1=esn_dict[1]; S2=esn_dict[2]; S3=esn_dict[3]
			S1t=S1[-1]; S2t=S2[-1]; S3t=S3[-1]
			a = 3*S1t - 3*S2t + S3t
			b = (alpha/(2*(1-alpha)**2)) * ((6-5*alpha)*S1t - 2*(5-4*alpha)*S2t + (4-3*alpha)*S3t)
			c = (alpha**2/(2*(1-alpha)**2)) * (S1t-2*S2t+S3t)
			fittedvalues=np.round(S3) # 将预测的销量四舍五入
			error=self.error_fun(y_test=array(X),y_predict=fittedvalues)
			if error<self.best_error:
				self.best_error=error
				self.best_alpha=alpha
				self.a=a
				self.b=b
				self.c=c
				self.fittedvalues=fittedvalues

	def get_fittedvalues(self):   # 预测拟合值
		return self.fittedvalues  # array

	def predict(self,forcast_period=2):
		t=arange(1,forcast_period+1)
		y_predict= self.a+self.b*t+self.c*t**2
		return np.round(y_predict) # array

# 变量定义 -------------------------------------------------------------
timeseries_methods={'AR':ts_AR,'MA':ts_MA,'ARMA':ts_ARMA,'ARIMA':ts_ARIMA,'SARIMAX':ts_SARIMAX,'AUTO_ARIMA':ts_AUTO_ARIMA,'SMA':ts_SMA,'WMA':ts_WMA,'ES2':ts_ES2,'ES3':ts_ES3}



##############################################################################
# 测试代码
if __name__=='__main__':
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


	df_obj=pd.DataFrame(y) # 将Series(name=quantity)转化为DataFrame
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
	# ts_diff = y.diff(1) #进行d阶差分
	# ts_diff.dropna(inplace=True) #丢掉缺失值,If True, do operation inplace and return None.
	# lbvalue,pvalue2=acorr_ljungbox(ts_diff,lags=1) #白噪声检验结果
	# adf,pvalue1,usedlag,nobs,critical_values,icbest= adfuller(ts_diff) #ADF检验
	# rule_1=(adf<critical_values['1%'] and adf<critical_values['5%'] and adf<critical_values['10%'] and pvalue1<0.01) 
	# rule_2=(pvalue2<p_value_shreshold)
	# if rule_1 and rule_2:
	# 	isStationarity=True
	# 	print('111:isStationarity')

	ts_diff = y_series_sub.diff(1) #进行d阶差分
	ts_diff.dropna(inplace=True) #丢掉缺失值,If True, do operation inplace and return None.
	lbvalue,pvalue2=acorr_ljungbox(ts_diff,lags=1) #白噪声检验结果
	adf,pvalue1,usedlag,nobs,critical_values,icbest= adfuller(ts_diff) #ADF检验
	rule_1=(adf<critical_values['1%'] and adf<critical_values['5%'] and adf<critical_values['10%'] and pvalue1<0.01) 
	rule_2=(pvalue2<p_value_shreshold)
	print(rule_1,rule_2)

	ts_diff = y_series_sub.diff(2) #进行d阶差分
	ts_diff.dropna(inplace=True) #丢掉缺失值,If True, do operation inplace and return None.
	lbvalue,pvalue2=acorr_ljungbox(ts_diff,lags=1) #白噪声检验结果
	adf,pvalue1,usedlag,nobs,critical_values,icbest= adfuller(ts_diff) #ADF检验
	rule_1=(adf<critical_values['1%'] and adf<critical_values['5%'] and adf<critical_values['10%'] and pvalue1<0.01) 
	rule_2=(pvalue2<p_value_shreshold)
	print(rule_1,rule_2)
	# if rule_1 and rule_2:
	# 	isStationarity=True
	# 	print('2222:isStationarity')
	# else:
	# 	print('not good')


	# model = sm.tsa.statespace.SARIMAX(y,
	# 					order=(1,0,1),
	# 		            seasonal_order=(1,0,1,7),
	# 		            enforce_stationarity=False,
	# 		            enforce_invertibility=False)
	# results_SARIMAX = model.fit(disp=False)
	# # pred = results_SARIMAX.get_prediction(start=pd.to_datetime('2018-05-03'), dynamic=False)
	
	# print(results_SARIMAX.summary())
	# y_pre=results_SARIMAX.predict()
	# y_fit=results_SARIMAX.forecast(10)
	# print(type(y_fit))





	# dd=pd.date_range('5/1/2018',periods=31,freq='d')
	# index4=range(3,31,4)
	# index7=range(6,31,7)
	# print(dd[index4])
	# print(dd[index7])

	# dd=pd.date_range('1/1/2016',periods=365,freq='d')
	# for d in dd:
	# 	if d.weekday() in [5,6]:
	# 		weekend=1
	# 	else:
	# 		weekend=0
	# 	print(d,weekend)


#测试ts_moving_average
# num=10
# ts=Series(np.random.randint(10,size=365),index=pd.date_range('1/1/2015',periods=365,freq='d'))
# print(ts)
# ma=ts_moving_average(ts,window=3,ts_test=None,forcast_period=5)
# print(ts.values)
# y_predict,y_forcast=ma.predict()
# print(y_predict)
# print(y_forcast)

##########################################################################
#测试ARIMA
'''
# 读取数据，pd.read_csv默认生成DataFrame对象，需将其转换成Series对象
df = pd.read_csv('AirPassengers.csv', encoding='utf-8', index_col='Month')
df.index = pd.to_datetime(df.index)  # 将字符串索引转换成时间索引
ts = df['x']  # 生成pd.Series对象
# print(ts.head())
ts=ts.astype(np.float64) #将其转化为float64

model=ts_ARMA(ts[:-10],ts_test=3,forcast_period=5)

y_predict,y_forcast=model.predict()
plt.plot(ts,color='green')
plt.plot(model.model.fittedvalues, color='red')
plt.plot(model.model.predict('1960-03-01', '1960-12-01', dynamic=True),color='magenta')
forcast=Series(model.model.forecast(10)[0],index=ts.index[-10:])
plt.plot(forcast,color='black')
plt.show()
# model=arima_model(ts[:-10])
# y_predict,y_forcast=model.predict()
# print('use search:',model.p,model.d,model.q)
# plt.plot(ts,color='green')
# # # plt.plot(model.ts_diff,color='darkcyan')
# plt.plot(model.fittedModel.fittedvalues, color='red')
# # # plt.plot(model.fittedModel.predict('1960-03-01', '1960-12-01', dynamic=True),color='black')
# forcast=Series(model.fittedModel.forecast(10)[0],index=ts.index[-10:])
# # print(forcast)
# plt.plot(forcast,color='black')
# plt.show()
'''