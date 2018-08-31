#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 18:03:21
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

from pandas.tseries.offsets import Day
# 导入自定义的包
from algorithm.demand_forecast.feature_engineering import *
from algorithm.demand_forecast.timeseries_models import *
from algorithm.demand_forecast.save_load_forecast_model import *
'''
#变量regression_methods来自自定义包:regression_models
regression_methods={'DTR':DecisionTreeRegressor,'LR':LinearRegression,'SVR':SVR,'KNN':KNeighborsRegressor,
'ABR':AdaBoostRegressor,'RFR':RandomForestRegressor,'GBRT':GradientBoostingRegressor}

#变量evaluation_methods来自自定义包:feature_engineering
evaluation_methods={'MSE':prediction_MSE,'RMSE':prediction_RMSE,'MAE':prediction_MAE,'MAPE':prediction_MAPE}
'''

def integrated_timeseries_exog_model(
	isIntelligent=True,
	sku_id='',
	df=None,
	forecast_model='ARIMA_exog',
	evaluation='MAPE',
	length_merge=7,
	period=4,
	retrain=True):
	'''
	回归的预测方法
	--input parameters--
	df:预测的输入数据--DataFrame(训练+预测)
	forecast_model:预测模型
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

	exogenous_variables=['sale_price',
						'purchase_price',
						'promotion_1',
						'promotion_2',
						'promotion_3',
						'promotion_4',
						'promotion_5',
						'on_hand_quantity'
						]
	
	# 保留y的原始值Series和平均值Series
	df_tmp=df_tmp.set_index(['date'])   # 将date列设置为索引,仍然为DataFrame
	y_series_mean=df_tmp['week_num']     # y的平均值Series
	y_series_original=df_tmp['quantity'] # y的原始值Series
	y_series_mean=y_series_mean[:-predict_days]
	y_series_original=y_series_original[:-predict_days]

	# 选择外来特征列
	df_tmp=df_tmp[exogenous_variables]
	# 特征独热编码,将所有字符串类型的特征均做热编码
	df_tmp=code_dummies(df_tmp)
	# 取出输入数据X
	X=df_tmp.values.astype(np.float32) 
	# 数据的标准化
	X=normalization(data_X=X)
	X_train=X[:-predict_days,:]
	X_test=X[-predict_days:,:]

	# (2) 模型训练及滚动预测
	# 减去y的按星期平均值Series
	y_series_sub=y_series_original-y_series_mean
	if retrain:
		model=timeseries_exog_methods[forecast_model](ts_train=y_series_sub,exog=X_train,error_fun=evaluation_methods[evaluation])
		model.fit()
		if isIntelligent is True:
			save_forecast_model(id=sku_id,model_name=forecast_model,model=model)
	else:
		# 注意要调用已有的模型,则输入特征不能改变,否则预测会报错
		model=load_forecast_model(id=sku_id,model_name=forecast_model)
		if model is None:
			print('[INFO]:sku_id({})的{}模型加载失败,重新训练'.format(sku_id,forecast_model))
			model=timeseries_exog_methods[forecast_model](ts_train=y_series_sub,exog=X_train,error_fun=evaluation_methods[evaluation])
			model.fit()
			save_forecast_model(id=sku_id,model_name=forecast_model,model=model)
	# print('$'*20)
	# print(model.order,model.seasonal_order)
	y_real=y_series_original
	y_fit=model.get_fittedvalues()# 返回ndarray
	delete_num=len(y_real)-len(y_fit)
	y_real=y_real[delete_num:]
	y_fit=y_fit+array(y_series_mean[delete_num:])
	y_predict=model.predict(predict_days,exog=X_test)+array(y_series_mean[-predict_days:])
	# 按周期合并
	y_real=timeseries_merge(list(y_real),length_merge=length_merge)
	y_fit=timeseries_merge(list(y_fit),length_merge=length_merge)
	y_predict=timeseries_merge(list(y_predict),length_merge=length_merge)
	# 计算训练数据的拟合误差
	error_fit=evaluation_methods[evaluation](y_test=array(y_real),y_predict=array(y_fit))
	#四舍五入保留2位小数
	y_real=list(np.round(y_real,2))
	y_fit=list(np.round(y_fit,2))
	y_predict=list(np.round(y_predict,2))
	error_fit=np.round(error_fit,2) 

	return y_real,y_fit,y_predict,error_fit