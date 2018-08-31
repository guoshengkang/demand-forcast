#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-24 16:22:29
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import datetime
import pandas as pd
import sys
sys.path.append('../')
from base.base_module import BaseModel
from model.optimization.forecast import DemandForecast

class ForecastAllocationService():
    def __init__(
        self,
        calculate_record_id = 1,     # 服务调用id
        warehouse_id = 1,            # 仓库id
        id_type = 'sku',
        period = 4,                  # 预测周期数
        length_merge = 7,            # 合并区间长度
        date_start = '2018-01-28',   # 开始日期
        date_end = '2018-04-04'      # 结束日期
        ):
        # 计算预测天数
        predict_days=length_merge*period
        date_end_history=datetime.datetime.strptime(date_end,'%Y-%m-%d')
        # print(type(date_end_history)) # <class 'datetime.datetime'>
        date_start_forecast=date_end_history+datetime.timedelta(1)
        date_start_forecast=str(date_start_forecast)[:10]
        date_end_forecast=date_end_history+datetime.timedelta(predict_days)
        date_end_forecast=str(date_end_forecast)[:10]
        self.calculate_record_id=calculate_record_id 
        self.warehouse_id=warehouse_id
        self.id_type=id_type
        self.period=period
        self.length_merge=length_merge
        self.date_start=date_start
        self.date_end=date_end
        self.date_start_forecast=date_start_forecast
        self.date_end_forecast=date_end_forecast

    def get_demand_proportion(self):
        """
        从 ios_sale_order 和 ios_sale_order_line 表中获取产品在某一短时间的销量
        """
        date_end_train=datetime.datetime.strptime(self.date_end,'%Y-%m-%d')
        # 上一期的结束时间
        date_end_last_period=date_end_train-datetime.timedelta(1)
        date_end_last_period=str(date_end_last_period)[:10]
        # 上一期的开始时间
        date_start_last_period=date_end_train-datetime.timedelta(self.length_merge)
        date_start_last_period=str(date_start_last_period)[:10]

        sql="""
        SELECT
        id,
        store_id,
        quantity/SUM(quantity)over(partition by id) AS demand_proportion
        FROM
        (SELECT
        ol.{1}_id AS id,
        o.store_id AS store_id,
        SUM(ol.quantity) AS quantity
        FROM ios_sale_order AS o
        INNER JOIN ios_sale_order_line AS ol
        ON o.order_id=ol.order_id
        INNER JOIN ios_base_store AS s
        ON s.store_id=o.store_id
        WHERE s.warehouse_id={0} 
        AND o.sale_date>='{2}'
        AND o.sale_date<='{3}' 
        AND o.status=1
        AND ol.quantity>0
        GROUP BY o.store_id,ol.{1}_id
        ) AS t
        """.format(self.warehouse_id,self.id_type,date_start_last_period,date_end_last_period)
        # print(sql)
        rows = BaseModel.raw(sql)
        demand_proportion_dict = dict()
        if len(rows)>=1:    
            for row in rows:
                id=int(row.id)
                store_id=int(row.store_id)
                demand_proportion=round(float(row.demand_proportion),9)
                if id in demand_proportion_dict:
                    demand_proportion_dict[id][store_id]=demand_proportion
                else:
                    demand_proportion_dict[id]={}
                    demand_proportion_dict[id][store_id]=demand_proportion
        else:
            print('[INFO]:找不到warehouse_id({})的销量分摊比例信息!!!'.format(self.warehouse_id))
        # print(demand_proportion_dict)
        return demand_proportion_dict

    def allocation(self,dict_list=None):
        '''
        预测分摊并保存结果
        '''
        demand_proportion_dict=self.get_demand_proportion()
        insert_values=[]
        calculate_record_id=self.calculate_record_id

        for dic in dict_list:
            id=int(dic.get("id",None))
            code=dic.get("code",None)
            store_proportion_dict=demand_proportion_dict.get(id,None)
            if store_proportion_dict is None:
                continue
            for store_id in store_proportion_dict:
                proportion=store_proportion_dict[store_id]
                if not code:
                    forecast_dates=pd.date_range(start=self.date_start_forecast,end=self.date_end_forecast,freq='d')
                    # 写入预测数据
                    y_predict=dic.get("y_predict",None)
                    for k in range(self.period):
                        start_date=str(forecast_dates[k*self.length_merge])[:10]
                        end_date=str(forecast_dates[(k+1)*self.length_merge-1])[:10]
                        tmp_dict={
                        'calculate_record_id':calculate_record_id,
                        'warehouse_id':self.warehouse_id,
                        'store_id':store_id,
                        'sku_id':id,
                        'code':code, 
                        'desc':dic.get("desc",None),
                        'model':dic.get("model",None),
                        'data_type':2,
                        'start_date':start_date,
                        'end_date':end_date,
                        'quantity':0 if y_predict[k]<0 else y_predict[k]*proportion
                        }
                        insert_values.append(tmp_dict)
                else:
                    tmp_dict={
                    'calculate_record_id':calculate_record_id,
                    'warehouse_id':self.warehouse_id,
                    'store_id':store_id,
                    '{}_id'.format(self.id_type):id,
                    'code':code,
                    'desc':dic.get("desc",None),
                    'model':dic.get("model",None),
                    'data_type':None,
                    'start_date':None,
                    'end_date':None,
                    'quantity':None
                    }
                    insert_values.append(tmp_dict)
        # print('$'*20)
        # print(insert_values)
        DemandForecast.insert_many(insert_values).execute()

########################################################################################
# 测试代码
if __name__=='__main__':
    fas=ForecastAllocationService(
        calculate_record_id = 1,    # 服务调用id
        warehouse_id = 1,            # 仓库id
        id_type = 'sku',
        period = 4,                        # 预测周期数
        length_merge = 300,            # 合并区间长度
        date_start = '2017-01-28',  # 开始日期
        date_end = '2018-04-04'        # 结束日期
        )
    demand_proportion_dict=fas.get_demand_proportion()
    print(demand_proportion_dict)