#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-27 14:04:18
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})
import sys
sys.path.append('../')
import json
# 导入自定义的包
from process.demand_forecast_process import DemandForecastProcess
from forecast_allocation_service import ForecastAllocationService
class DemandForecastService():
    def __init__(
        self,
        calculate_record_id = 1,                     # 服务调用id
        # 项目编号
        organization_id = 1,
        warehouse_id = 1,                  # 仓库id
        id_type = 'sku',
        # 影响预测天数的参数
        period = 7,                        # 预测周期数
        length_merge = 1,                  # 合并区间长度
        # 影响历史数据的参数
        date_start = '2018-01-28',         # 开始日期
        date_end = '2018-04-04',           # 结束日期
        # 影响预测算法的参数
        isIntelligent=False,
        forecast_model='WMA',
        evaluation='RMSE'
        ):
        # 服务调用id
        self.calculate_record_id=calculate_record_id
        # 项目编号
        self.organization_id=organization_id
        self.warehouse_id=warehouse_id
        self.id_type=id_type
        # 影响预测天数的参数
        self.period=period
        self.length_merge=length_merge
        # 影响历史数据的参数
        self.date_start=date_start
        self.date_end=date_end
        # 影响预测算法的参数
        self.isIntelligent=isIntelligent
        self.forecast_model=forecast_model
        self.evaluation=evaluation

    def run(self):
        '''
        result = {
            'calculate_record_id': 1,
            'status': 1. 计算完成(完全成功) 2. 失败/完全无法计算  3. 部分计算成功(部分出错或无法计算)
            'calculate_msg': 信息 'OK', '失败信息', '部分计算成功', '格式内容不固定, 自己随便写'
            'calculate_error_code': '' # 暂时为空
            }
        '''
        # 默认值
        result = {
            'calculate_record_id': self.calculate_record_id,
            'status': 1,
            'calculate_msg':'OK',
            'calculate_error_code': '' # 暂时为空
            }
        # try:
        # 初始化DemandForecastProcess类
        dfp=DemandForecastProcess(
            calculate_record_id=self.calculate_record_id,
            organization_id=self.organization_id,
            warehouse_id=self.warehouse_id,
            id_type = self.id_type,
            period=self.period,
            length_merge=self.length_merge,
            date_start = self.date_start,
            date_end = self.date_end,
            isIntelligent=self.isIntelligent,
            forecast_model=self.forecast_model, 
            evaluation=self.evaluation
            )
        list_result=dfp.prediction()

        for dic in list_result:
            code=dic.get("code",None)
            if code is not None:
                result['status']=3
                result['calculate_msg']='部分计算成功'
                break

        # 预测分摊,并写入数据库
        fas=ForecastAllocationService(
            calculate_record_id = self.calculate_record_id,
            warehouse_id = self.warehouse_id,
            id_type = self.id_type,
            period=self.period,
            length_merge = self.length_merge,
            date_start = self.date_start,
            date_end = self.date_end)
        print('[INFO]:{:-^30}'.format('开始计算门店预测分摊并保存数据库'))
        fas.allocation(dict_list=list_result)
        print('[INFO]:{:-^30}'.format('完成计算门店预测分摊并保存数据库'))
        print('^_^^_^:{:*^30}'.format('居然没有遇到Bug,你太棒了！'))
        # except Exception as e:
        #         result['status']=2
        #         result['calculate_msg']='{}'.format(repr(e)) # repr(e)给出较全的异常信息，包括异常信息的类型
        #         print('^_^^_^:{:*^30}'.format('只是遇到了一个小小的Bug而已,没关系,改一下就好了！'))
        
        print('打印返回结果:',result)
        return result


########################################################################################
# 测试代码
if __name__=='__main__':
    import os
    import datetime
    starttime = datetime.datetime.now()   

    dfs=DemandForecastService(
        calculate_record_id=31,
        # 项目编号
        organization_id = 1,
        warehouse_id = 1,                  # 仓库id
        # 影响预测天数的参数
        period = 4,                        # 预测周期数
        length_merge = 7,                  # 合并区间长度
        # 影响历史数据的参数
        date_start = '2018-01-28',         # 开始日期
        date_end = '2018-04-04',           # 结束日期
        # 影响预测算法的参数
        isIntelligent=True,
        forecast_model='WMA',
        evaluation='RMSE'
        )
    json_str=dfs.run()
    #####################################################
    endtime = datetime.datetime.now()
    print((endtime - starttime),"time used!!!") #0:00:00.280797