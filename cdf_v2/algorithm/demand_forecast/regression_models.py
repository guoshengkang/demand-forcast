#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-17 14:26:36
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import sys
import numpy as np
#回归模型
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression,BayesianRidge,ElasticNet
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import AdaBoostRegressor,RandomForestRegressor,GradientBoostingRegressor
# from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
import tensorflow as tf

# 自定的包
# from feature_engineering import *
'''
该自定义包定义和回归模型相关的函数和变量
'''

# 函数定义
# def model_regression(X_train,y_train,X_test,y_test,X_forcast,clf,length_merge=2,period=5,error_fun=None):
# 	'''
# 	训练gbrt模型,并对测试数据和预测数据进行预测
# 	'''
# 	clf.fit(X_train,y_train)
# 	y_predict = clf.predict(X_test)
# 	y_forcast = clf.predict(X_forcast)

# 	# 根据合并长度,合并预测结果
# 	y_forcast_merge=[sum(y_forcast[k*length_merge:k*length_merge+length_merge]) for k in range(period)]
# 	# 将预测的销量四舍五入
# 	y_predict=np.round(y_predict)
# 	y_forcast_merge=np.round(y_forcast_merge)
# 	y_test=timeseries_merge(list(y_test),length_merge=length_merge) #时间序列的合并
# 	y_predict=timeseries_merge(list(y_predict),length_merge=length_merge) #时间序列的合并
# 	y_forcast=list(y_forcast_merge)
# 	error=error_fun(y_test=array(y_test),y_predict=array(y_predict))
# 	return y_test,y_predict,y_forcast,error # 返回列表



# 变量定义
regression_methods={'DTR':DecisionTreeRegressor,'LR':LinearRegression,'SVR':SVR,'KNN':KNeighborsRegressor,
'ABR':AdaBoostRegressor,'RFR':RandomForestRegressor,'GBRT':GradientBoostingRegressor,'BR':BayesianRidge,'ETC':ElasticNet}