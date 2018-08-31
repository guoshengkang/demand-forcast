#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-06 15:02:11
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

# 导入非自定义的包
import demjson
import pandas as pd
import datetime
# 导入自定义的包 algorithm.demand_forecast.
from algorithm.demand_forecast.intelligent_model import *
from algorithm.demand_forecast.nonintelligent_model import *


class DemandForecastAlgorithm():
	def __init__(
		self, 
		# True/False类型:是否调用智能算法
		isIntelligent=False,
		# DataFrame类型:商品相关的预测输入数据
		df_input_data=None,
		# DataFrame类型:时间相关的预测输入数据
		df_time_data=None,
		# 字符串类型:获取数据的开始日期
		date_start=None,
		# 字符串类型:获取数据的结束日期
		date_end=None,
		# 字典类型:获取sku的需求类别
		demand_class_dict=None,
		# 字典类型:上一期的预测误差
		last_predicted_error=None,
		# 字符串类型:选择预测模型
		forecast_model = 'WMA',
		# 字符串类型:选择的预测评估指标
		evaluation = 'MAPE',
		# int类型:周期的合并长度
		length_merge=1,
		# int类型:预测的周期数
		period=7):
		self.isIntelligent=isIntelligent
		self.input_data_df=df_input_data
		self.config_data_df=df_time_data
		self.date_start=datetime.datetime.strptime(date_start,'%Y-%m-%d')
		self.date_end=datetime.datetime.strptime(date_end,'%Y-%m-%d')
		self.demand_class_dict=demand_class_dict
		self.last_predicted_error=last_predicted_error
		self.forecast_model=forecast_model
		self.evaluation=evaluation
		self.length_merge=length_merge
		self.period=period

	def run(self):
		if self.isIntelligent:
			result_json=intelligent_model(
				input_data_df=self.input_data_df,
				config_data_df=self.config_data_df,
				date_start=self.date_start,
				date_end=self.date_end,
				demand_class_dict=self.demand_class_dict,
				last_predicted_error=self.last_predicted_error,
				forecast_model=self.forecast_model,
				evaluation=self.evaluation,
				length_merge=self.length_merge,
				period=self.period)
		else:
			result_json=nonintelligent_model(
				input_data_df=self.input_data_df,
				config_data_df=self.config_data_df,
				date_start=self.date_start,
				date_end=self.date_end,
				demand_class_dict=self.demand_class_dict,
				last_predicted_error=self.last_predicted_error,
				forecast_model=self.forecast_model,
				evaluation=self.evaluation,
				length_merge=self.length_merge,
				period=self.period)
		return result_json

########################################################################################
# 测试代码
if __name__=='__main__':
	# 获取输入数据 input_data_df,config_data_df,demand_class_dict
	from get_data_from_db import *

	dfa=DemandForecastAlgorithm(
            isIntelligent=False,
            df_input_data=input_data_df,
            df_time_data=config_data_df,
            date_start='2018-01-28',
            date_end='2018-04-04',
            demand_class_dict=demand_class_dict,
            forecast_model='ARIMA',
            evaluation='RMSE',
            length_merge=7,
            period=4)
	json_result=dfa.run()
	print(json_result)


# timeseries_methods={'AR':ts_AR,'MA':ts_MA,'ARMA':ts_ARMA,'ARIMA':ts_ARIMA,'SARIMA':ts_SARIMA,'HWES':ts_holtwinters_ES}
# timeseries_exog_methods={'ARIMAX':ts_ARIMAX,'SARIMAX':ts_SARIMAX}
# timeseries_merge_methods={'SMA':ts_SMA,'WMA':ts_WMA,'ES2':ts_ES2,'ES3':ts_ES3,'SES':ts_SES}
# regression_methods={'DTR':DecisionTreeRegressor,'LR':LinearRegression,'SVR':SVR,'KNN':KNeighborsRegressor,
# 'ABR':AdaBoostRegressor,'RFR':RandomForestRegressor,'GBRT':GradientBoostingRegressor,'BR':BayesianRidge,'ETC':ElasticNet}