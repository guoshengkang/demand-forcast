#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-27 14:04:18
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})
import sys
sys.path.append('../')
import json
# 导入自定义的包
from process.demand_forecast_process import *

class DemandForecastService():
    def __init__(
        self,
        # 项目编号
        organization_id=1,
        # 影响预测天数的参数
        period = 7,                        # 预测周期数
        forecast_period_range_id = 3,      # 预测周期合并区间(合并方式) 1: 订货周期, 2: 订货批量 3: 天 4:周 5:月 6: 季度
        length_merge = 1,                  # 合并区间长度
        # 影响历史数据的参数
        warehouse_id_list =  [1],          # 仓库id
        calculate_dimension_id = 3,        # 计算维度 1: SKU级别, 2: SKC级别, 3: 商品级别  order_line合并的时候标准不同
        calculate_range_id = 1,            # 计算范围 1: 全部, 2: 快流件 3: 慢流件  4: 手动选择
        date_start = '2018-01-28',         # 开始日期
        date_end = '2018-04-25',           # 结束日期
        forecast_by='store_id',            # 按照什么来预测 'store_id' or 'warehouse_id'
        id=1,                              # 'store_id' or 'warehouse_id'
        # 影响预测算法的参数
        isIntelligent=True,
        forcast_models=['WMA'],
        evaluation='MAPE',
        ):
        # 项目编号
        self.organization_id=organization_id
        # 影响预测天数的参数
        self.period=period
        self.forecast_period_range_id=forecast_period_range_id
        self.length_merge=length_merge
        # 影响历史数据的参数
        self.warehouse_id_list=warehouse_id_list
        self.calculate_dimension_id=calculate_dimension_id
        self.calculate_range_id=calculate_range_id
        self.date_start=date_start
        self.date_end=date_end
        self.forecast_by=forecast_by
        self.id=id
        # 影响预测算法的参数
        self.isIntelligent=isIntelligent
        self.forcast_models=forcast_models
        self.evaluation=evaluation

    def run(self):
        # 初始化DemandForecastProcess类
        dfp=DemandForecastProcess(
        	# 影响预测天数的参数
        	period=self.period,
            forecast_period_range_id=self.forecast_period_range_id,
            length_merge=self.length_merge,
            # 影响历史数据的参数
            warehouse_id_list=self.warehouse_id_list,
            calculate_dimension_id=self.calculate_dimension_id,
            calculate_range_id=self.calculate_range_id,
            date_start=self.date_start,
            date_end=self.date_end,
            forecast_by=self.forecast_by,
            id=self.id)
        # 根据参数要求获取预测的输入数据
        input_data_str, time_data_str,time2market=dfp.get_data()
        # 调用预测方法
        json_str=dfp.prediction(
        	isIntelligent=self.isIntelligent,
        	input_data_str=input_data_str,
        	time_data_str=time_data_str,
        	time2market=time2market,
        	forcast_models=self.forcast_models,
        	evaluation=self.evaluation)
        return json_str


########################################################################################
# 测试代码
if __name__=='__main__':
    import datetime
    starttime = datetime.datetime.now()   
    ###################################################### 
    dfs=DemandForecastService(
    # 影响预测天数的参数
    period = 7,                        # 预测周期数
    forecast_period_range_id = 3,      # 预测周期合并区间(合并方式) 1: 订货周期, 2: 订货批量 3: 天 4:周 5:月 6: 季度
    length_merge = 1,                  # 合并区间长度
    # 影响历史数据的参数
    warehouse_id_list =  [1],          # 仓库id
    calculate_dimension_id = 3,        # 计算维度 1: SKU级别, 2: SKC级别, 3: 商品级别  order_line合并的时候标准不同
    calculate_range_id = 1,            # 计算范围 1: 全部, 2: 快流件 3: 慢流件  4: 手动选择
    date_start = '2018-01-28',         # 开始日期
    date_end = '2018-04-25',           # 结束日期
    forecast_by='store_id',            # 按照什么来预测 'store_id' or 'warehouse_id'
    id=1,                              # 'store_id' or 'warehouse_id'
    # 影响预测算法的参数
    isIntelligent=True,
    forcast_models=['WMA'],
    evaluation='MAPE',
    )

    json_str=dfs.run()

    json_list=json.loads(json_str)
    for x in json_list:
        print(x)
    #####################################################
    endtime = datetime.datetime.now()
    print((endtime - starttime),"time used!!!") #0:00:00.280797