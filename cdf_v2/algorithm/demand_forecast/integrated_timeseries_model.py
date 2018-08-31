#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 18:03:21
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

# 导入自定义的包
from algorithm.demand_forecast.feature_engineering import *
from algorithm.demand_forecast.timeseries_models import *
from algorithm.demand_forecast.save_load_forecast_model import *
'''
#变量timeseries_methods来自自定义包:timeseries_models
timeseries_methods={'AR':ts_MA,'MA':ts_MA,'ARMA':ts_ARMA,'ARIMA':ts_ARIMA}
#变量evaluation_methods来自自定义包:feature_engineering
evaluation_methods={'MSE':prediction_MSE,'RMSE':prediction_RMSE,'MAE':prediction_MAE,'MAPE':prediction_MAPE}
'''

def integrated_timeseries_model(
	isIntelligent=True,
	sku_id='',
	df=None,
	forecast_model='ARIMA',
	evaluation='MAPE',
	length_merge=1,
	period=7,
	retrain=True):
	'''
	时间序列的预测方法
	--input parameters--
	df:预测的输入数据--DataFrame(训练+预测)
	forecast_model:预测模型--str
	evaluation:预测评估方法--str
	length_merge:数据合并的天数--int
	period:预测的周期--int
	'''
	df_tmp=df.copy()
	# 预测天数
	predict_days=length_merge*period

	# (1) 数据预处理
	index_train=df_tmp.index[:-predict_days] # 只取训练数据做预处理
	# 在训练集中求按星期的销量平均
	df_tmp=df_tmp.ix[index_train,['quantity','date']]
	df_tmp['week_num']=df_tmp['date'].map(lambda x: x.weekday())
	y_avg=df_tmp.groupby('week_num').quantity.aggregate([np.mean]) # 返回DataFrame
	y_avg=y_avg.ix[:,0] # 取第1列,等价于y_avg['mean'],返回Series
	# 将week_num列的值映射为按星期的平均销量
	df_tmp['week_num']=df_tmp['week_num'].map(lambda x: y_avg[x])  
	df_tmp=df_tmp.set_index(['date'])    # 将date列设置为索引,仍然为DataFrame
	# y的按星期平均值Series
	if forecast_model=='ARIMA' or forecast_model=='SARIMAX':
		# 只有在ARIMA模型中,y减去按星期的平均值
		y_series_mean=df_tmp['week_num']
	else:
		# ARMA模型中使用log差分,值不能为负,因此不减去按星期的平均值
		# 而在移动平均中,y减去按星期的平均值并不能带来优化,反而可能导致训练时计算MAPE,分母为0
		y_series_mean=df_tmp['week_num']-df_tmp['week_num']
	# y的原始值Series
	y_series_original=df_tmp['quantity']
	# 减去y的按星期平均值Series
	y_series_sub=y_series_original-y_series_mean

	# (2) 模型训练及滚动预测
	if retrain:
		model=timeseries_methods[forecast_model](ts_train=y_series_sub,error_fun=evaluation_methods[evaluation])
		model.fit()
		if isIntelligent is True:
			save_forecast_model(id=sku_id,model_name=forecast_model,model=model)
	else:
		# 注意要调用已有的模型,则输入特征不能改变,否则预测会报错
		model=load_forecast_model(id=sku_id,model_name=forecast_model)
		if model is None:
			print('[INFO]:sku_id({})的{}模型加载失败,重新训练'.format(sku_id,forecast_model))
			model=timeseries_methods[forecast_model](ts_train=y_series_sub,error_fun=evaluation_methods[evaluation])
			model.fit()
			save_forecast_model(id=sku_id,model_name=forecast_model,model=model)	
	# print(model.order,model.seasonal_order)
	y_real=y_series_original
	y_fit=model.get_fittedvalues()# 返回ndarray
	delete_num=len(y_real)-len(y_fit)
	y_real=y_real[delete_num:]
	y_fit=y_fit+array(y_series_mean[delete_num:])
	y_predict=model.predict(predict_days)+array(y_series_mean[-predict_days:])
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

