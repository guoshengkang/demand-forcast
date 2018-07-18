#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-27 14:04:18
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})
import sys
sys.path.append('../')
import json
# 导入自定义的包
from demand_forecast_process import *
import datetime
starttime = datetime.datetime.now()   
###################################################### 
# 影响预测天数的参数
period = 3                       # 预测周期数
forecast_period_range_id = 3     # 预测周期合并区间(合并方式) 1: 订货周期, 2: 订货批量 3: 天 4:周 5:月 6: 季度
length_merge = 7                 # 合并区间长度
# 影响历史数据的参数
warehouse_id_list =  [1]         #[80,81,82] # 仓库id
calculate_dimension_id = 3       # 计算维度 1: SKU级别, 2: SKC级别, 3: 商品级别  order_line合并的时候标准不同
calculate_range_id = 1           # 计算范围 1: 全部, 2: 快流件 3: 慢流件  4: 手动选择
date_start = '2018-01-28'        # 开始日期
date_end = '2018-05-02'          # 结束日期

dfp=DemandForecastProcess(
	# 影响预测天数的参数
	period=period,
    forecast_period_range_id=forecast_period_range_id,
    length_merge=length_merge,
    # 影响历史数据的参数
    warehouse_id_list=warehouse_id_list,
    calculate_dimension_id=calculate_dimension_id,
    calculate_range_id=calculate_range_id,
    date_start=date_start,
    date_end=date_end,
    forecast_by='store_id',
    id=1
    )

input_data_str, time_data_str,time2market=dfp.get_data()

# 决定算法的参数
isIntelligent=True
forcast_models=['GBRT']   
evaluation='MAPE'  

json_str=dfp.prediction(
	isIntelligent=isIntelligent,
	input_data_str=input_data_str,
	time_data_str=time_data_str,
	time2market=time2market,
	forcast_models=forcast_models,
	evaluation=evaluation)

json_list=json.loads(json_str)
for x in json_list:
 	print(x)
#####################################################
endtime = datetime.datetime.now()
print((endtime - starttime),"time used!!!") #0:00:00.280797