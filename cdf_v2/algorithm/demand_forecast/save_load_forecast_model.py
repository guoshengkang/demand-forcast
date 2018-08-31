#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-21 09:37:59
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
from sklearn.externals import joblib

conf_name="algorithm"
if os.path.exists(conf_name):  # 在项目根目录下启动时, 读取usms.conf文件
	conf_name = conf_name
elif os.path.exists("../"+conf_name):  # 在根目录下级目录下运行文件时, 读取../usms.conf文件
	conf_name = "../"+conf_name
elif os.path.exists("../../"+conf_name):  # 在根目录下下级目录下运行文件时, 读取../../usms.conf文件
	conf_name = "../../"+conf_name
else:
	print('[INFO]:{:-^30}'.format('未找到保存模型的目录！！！'))

if os.name == "nt":
	# root_path = "..\\algorithm\\demand_forecast\\saved_models\\"
	root_path=os.path.join(conf_name, "demand_forecast\\saved_models\\")
else:
	# root_path = "../algorithm/demand_forecast/saved_models/"
	root_path=os.path.join(conf_name, "demand_forecast/saved_models/")

def save_forecast_model(id='44117',model_name='WMA',model=None):
	'''
	id:产品id
	model_name:模型名称
	'''
	# root_path=r"C:\Users\Kang\Desktop\model_management\saved_models"
	file_name=id+'_'+model_name+'.m' # e.g., 44117_WMA.m
	model_path=os.path.join(root_path, file_name)
	# 模型的保存
	try:
		joblib.dump(model, model_path)
	except Exception as e:
		print('[ERROR]:sku_id({})的{}模型保存失败({})'.format(id,model_name,e))
		# 注意保存失败,但是还是会产生一个同名的文件,因此需要删掉
		if os.path.exists(model_path):
			os.remove(model_path) # 删除文件
	
def load_forecast_model(id='44117',model_name='WMA'):
	'''
	id:产品id
	model_name:模型名称
	'''
	# root_path=r"C:\Users\Kang\Desktop\model_management\saved_models"
	file_name=id+'_'+model_name+'.m' # e.g., 44117_WMA.m
	model_path=os.path.join(root_path, file_name)
	# 模型的加载
	# model = joblib.load(model_path)
	try:
		model = joblib.load(model_path)
	except Exception as e:
		print('[ERROR]:sku_id({})的{}模型加载失败({})'.format(id,model_name,e))
		return None
	return model 


if __name__=='__main__':
	import numpy as np
	import pandas as pd
	from statsmodels.tsa import holtwinters
	# 测试指数平滑
	index=pd.date_range('5/1/2018',periods=20,freq='d')
	ts_train=pd.Series([1.0,2,3,4,3,6,3,7,3,5,1,2,3,4,3,6,3,7,3,5],index=index)
	train_model =  holtwinters.SimpleExpSmoothing(ts_train).fit(optimized=True)
	save_forecast_model(id='11111',model_name='SES',model=train_model)
	loaded_model=load_forecast_model(id='11111',model_name='SES')
	fittedvalues=loaded_model.predict(start=0,end=len(ts_train)-1)
	y_predict=loaded_model.forecast(4)
	print(fittedvalues)
	print(y_predict)



