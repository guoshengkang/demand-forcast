#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-10 09:15:56
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

'''
该文件定义了两个类
(1) PrepareDataSerive类根据参数要求,获取销量预测相关的输入数据
(2) DemandForecastProcess类根据销量预测输入数据,调用预测算法,输出预测结果
'''
# 测试代码时使用
import sys
sys.path.append('../')

# 导入非自定义的包
import json
import datetime
import pandas as pd
import numpy as np
# 导入自定义的包
from base.base_module import db,BaseModel
from model.optimization.forecast import DemandForecast
from algorithm.demand_forecast.demand_forecast_algorithm import *

class DemandForecastProcess():
    def __init__(
        self,
        calculate_record_id=1,
        # 项目编号
        organization_id=1,
        warehouse_id = 1,                  # 仓库id
        id_type = 'sku',                   # 产品id类型
        # 影响预测天数的参数
        period = 4,                        # 预测周期数
        length_merge = 7,                  # 合并区间长度
        # 影响历史数据的参数
        date_start = '2018-01-28',         # 开始日期
        date_end = '2018-04-25',            # 结束日期
        # 决定算法的参数
        isIntelligent=False,
        forecast_model='WMA',  
        evaluation='RMSE' 
        ):
        # 计算预测天数
        predict_days=length_merge*period
        date_end_train=datetime.datetime.strptime(date_end,'%Y-%m-%d')
        # print(type(date_end_train)) # <class 'datetime.datetime'>
        date_start_forecast=date_end_train+datetime.timedelta(1)
        date_start_forecast=str(date_start_forecast)[:10]
        date_end_forecast=date_end_train+datetime.timedelta(predict_days)
        date_end_forecast=str(date_end_forecast)[:10]
        # 调用id
        self.calculate_record_id=calculate_record_id
        self.organization_id=organization_id
        self.warehouse_id=warehouse_id
        self.id_type=id_type
        # 影响预测天数的参数
        self.period=period
        self.length_merge=length_merge
        # 影响历史数据的参数
        self.date_start=date_start
        self.date_end=date_end
        self.date_start_forecast=date_start_forecast
        self.date_end_forecast=date_end_forecast
        self.isIntelligent=isIntelligent
        self.forecast_model=forecast_model
        self.evaluation=evaluation

    def get_input_data(self):
        '''
        获取销量相关的输入数据
        '''
        sql="""
            SELECT
            t1.{3}_id AS id,
            Date(date) AS date,
            quantity,
            sale_price,
            purchase_price,
            promotion_1,
            promotion_2,
            promotion_3,
            promotion_4,
            promotion_5,
            product_status_1,
            product_status_2,
            product_status_3,
            product_status_4,
            on_hand_quantity
            FROM ios_optimization_product_feature_input AS t1
            INNER JOIN tmp_ios_optimization_demand_classification_2 AS t2
            ON t1.{3}_id=t2.{3}_id
            WHERE t1.warehouse_id={0}
            AND date>='{1}'
            AND date<='{2}'
            """.format(self.warehouse_id,self.date_start,self.date_end_forecast,self.id_type)
        df_input_data=pd.read_sql(sql, db)
        if df_input_data.empty:
            raise Exception('获取产品相关的特征数据为空!!!')
        # datetime.date类型转化为datetime.datetime类型
        df_input_data['date']=df_input_data['date'].map(lambda x: datetime.datetime.strptime(str(x),'%Y-%m-%d'))
        # print(df_input_data.head())
        # print(df_input_data.dtypes) 
        return df_input_data

    def get_time_data(self):
        '''
        获取时间相关的输入数据
        '''
        sql="""
            SELECT
            Date(work_day) AS date,
            holiday_type::VARCHAR AS holiday,
            month::VARCHAR AS season,
            is_weekend::INT AS weekend
            FROM ios_base_work_calendar
            WHERE work_day>='{0}'
            AND work_day<='{1}'
            """.format(self.date_start,self.date_end_forecast)
        df_time_data=pd.read_sql(sql, db)
        if df_time_data.empty:
            raise Exception('获取时间相关的特征数据为空!!!')
        # datetime.date类型转化为datetime.datetime类型
        df_time_data['date']=df_time_data['date'].map(lambda x: datetime.datetime.strptime(str(x),'%Y-%m-%d'))
        # print(df_time_data.head())
        # print(df_time_data.dtypes) # object,object,object,object
        # print(type(df_time_data['date'][0]),type(df_time_data['holiday'][0]),type(df_time_data['season'][0]),type(df_time_data['weekend'][0]))
        # <class 'datetime.datetime'> <class 'str'> <class 'str'> <class 'str'>
        return df_time_data

    def get_demand_class_data(self):
        '''
        获取需求分类数据
        '''
        sql="""
            SELECT
            DISTINCT
            {1}_id AS id,
            demand_class
            FROM ios_optimization_demand_classification
            WHERE warehouse_id={0}
            """.format(self.warehouse_id,self.id_type)
        rows = BaseModel.raw(sql)
        demand_class_dict = dict()
        for row in rows:
            id=str(row.id)
            demand_class=int(row.demand_class)
            demand_class_dict[id]=demand_class
        if not demand_class_dict: # 字典为空
            raise Exception('获取产品需求分类数据为空!!!')
        return demand_class_dict

    def get_last_predicted_error(self):
        '''
        获取产品上一期的预测误差
        '''
        date_end_train=datetime.datetime.strptime(self.date_end,'%Y-%m-%d')
        # 上一期的结束时间
        date_end_last_period=date_end_train-datetime.timedelta(1)
        date_end_last_period=str(date_end_last_period)[:10]
        # 上一期的开始时间
        date_start_last_period=date_end_train-datetime.timedelta(self.length_merge)
        date_start_last_period=str(date_start_last_period)[:10]
        # 获取上期的历史销量
        sql="""
            SELECT
            ol.{1}_id AS id,
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
            AND ol.status=1
            AND ol.quantity>0
            GROUP BY ol.{1}_id
            """.format(self.warehouse_id,self.id_type,date_start_last_period,date_end_last_period)
        # print(sql)    
        rows = BaseModel.raw(sql)
        history_quantity_dict = dict()
        for row in rows:
            id=int(row.id)
            quantity=float(row.quantity)
            history_quantity_dict[id]=quantity

        # 获取上期的预测销量
        sql="""
            SELECT
            df.{1}_id AS id,
            df.quantity AS quantity
            FROM ios_optimization_demand_forecast AS df
            INNER JOIN
                (select *
                FROM ios_base_calculate_record 
                WHERE type=4
                AND position('True' in params)>0
                ORDER BY gen_time DESC
                limit 1
                )  AS cr
            ON df.calculate_record_id=cr.record_id
            WHERE df.warehouse_id={0}
            AND df.store_id IS NULL
            AND df.code IS NULL
            AND df.start_date='{2}'
            AND df.end_date='{3}'
            """.format(self.warehouse_id,self.id_type,date_start_last_period,date_end_last_period)
        # print(sql)    
        rows = BaseModel.raw(sql)
        predict_quantity_dict = dict()
        for row in rows:
            id=int(row.id)
            quantity=float(row.quantity)
            predict_quantity_dict[id]=quantity
        # print(predict_quantity_dict)
        last_predicted_error=dict()
        if not predict_quantity_dict:
            print('[INFO]:获取上期的预测销量为空!!!')
        elif not history_quantity_dict:
            print('[INFO]:获取上期的历史销量为空!!!')
        else:
            for id in predict_quantity_dict:
                predicted_value=predict_quantity_dict.get(id,None)
                real_value=history_quantity_dict.get(id,None)
                if predicted_value is not None and real_value is not None:
                    if real_value==0:
                        error=0.0 if predicted_value==0 else 1.0
                    else:
                        error=abs(real_value-predicted_value)/real_value
                    last_predicted_error[id]=error
                else:
                    continue
        # print(last_predicted_error)
        return last_predicted_error

    def get_data(self):
        '''
        获取销量预测相关的所有输入数据
        '''
        df_input_data=self.get_input_data()
        df_time_data=self.get_time_data()
        demand_class_dict=self.get_demand_class_data()
        # 当选择智能算法时,才获取上期的预测误差
        if self.isIntelligent:
            last_predicted_error=self.get_last_predicted_error()
        else:
            last_predicted_error=None
        return df_input_data,df_time_data,demand_class_dict,last_predicted_error

    def save_predicted_results(self,dict_list=None):
        insert_values=[]
        calculate_record_id=self.calculate_record_id
        for dic in dict_list:
            id=int(dic.get("id",0))
            code=dic.get("code",None)
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
                    '{}_id'.format(self.id_type):id,
                    'code':code,
                    'desc':dic.get("desc",None),
                    'model':dic.get("model",None),
                    'data_type':2,
                    'start_date':start_date,
                    'end_date':end_date,
                    'quantity':0 if y_predict[k]<0 else y_predict[k]
                    }
                    insert_values.append(tmp_dict)
                # 写入真实和拟合数据
                y_real=dic.get("y_real",None)
                y_fit=dic.get("y_fit",None)
                train_dates=pd.date_range(end=self.date_end,freq='d',periods=self.length_merge*len(y_real))
                for k in range(len(y_real)):
                    start_date=str(train_dates[k*self.length_merge])[:10]
                    end_date=str(train_dates[(k+1)*self.length_merge-1])[:10]
                    tmp_dict={
                    'calculate_record_id':calculate_record_id,
                    'warehouse_id':self.warehouse_id,
                    '{}_id'.format(self.id_type):id,
                    'code':code,
                    'desc':dic.get("desc",None),
                    'model':dic.get("model",None),
                    'data_type':0,
                    'start_date':start_date,
                    'end_date':end_date,
                    'quantity':0 if y_real[k]<0 else y_real[k]
                    }
                    insert_values.append(tmp_dict)
                    start_date=str(train_dates[k*self.length_merge])[:10]
                    end_date=str(train_dates[(k+1)*self.length_merge-1])[:10]
                    tmp_dict={
                    'calculate_record_id':calculate_record_id,
                    'warehouse_id':self.warehouse_id,
                    '{}_id'.format(self.id_type):id,
                    'code':code,
                    'desc':dic.get("desc",None),
                    'model':dic.get("model",None),
                    'data_type':1,
                    'start_date':start_date,
                    'end_date':end_date,
                    'quantity':0 if y_fit[k]<0 else y_fit[k]
                    }
                    insert_values.append(tmp_dict)
            else:
                tmp_dict={
                'calculate_record_id':calculate_record_id,
                'warehouse_id':self.warehouse_id,
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
        DemandForecast.insert_many(insert_values).execute()

    def prediction(self):
        print('[INFO]:{:-^30}'.format('开始获取销量预测的输入数据'))
        df_input_data,df_time_data,demand_class_dict,last_predicted_error=self.get_data()
        print('[INFO]:{:-^30}'.format('完成获取销量预测的输入数据'))
        
        # 调用销量预测算法 demand_forecast_algorithm
        print('[INFO]:{:-^30}'.format('开始计算仓库销量预测'))
        dfa=DemandForecastAlgorithm(
            isIntelligent=self.isIntelligent,
            date_start=self.date_start,
            date_end=self.date_end,
            df_input_data=df_input_data,
            df_time_data=df_time_data,
            demand_class_dict=demand_class_dict,
            last_predicted_error=last_predicted_error,
            forecast_model=self.forecast_model,
            evaluation=self.evaluation,
            length_merge=self.length_merge,
            period=self.period)
        list_result=dfa.run()
        print('[INFO]:{:-^30}'.format('完成计算仓库销量预测'))
        # print(list_result)

        # 将仓库的销量预测结果写入结果写入数据库
        print('[INFO]:{:-^30}'.format('开始保存仓库销量预测结果'))
        self.save_predicted_results(dict_list=list_result)
        print('[INFO]:{:-^30}'.format('完成保存仓库销量预测结果'))
        return list_result

########################################################################################
# 测试代码
if __name__=='__main__':
    # 测试DemandForecastProcess类
    starttime = datetime.datetime.now()   
    ###################################################### 
    # 获取输入数据的参数
    organization_id=1
    calculate_record_id=2
    warehouse_id=1                   # 仓库id
    # 影响预测天数的参数
    period = 3                       # 预测周期数
    length_merge = 7                 # 合并区间长度
    # 影响历史数据的参数
    date_start = '2018-01-28'        # 开始日期
    date_end = '2018-04-12'          # 结束日期

    # 初始化类
    dfp=DemandForecastProcess(
        calculate_record_id=calculate_record_id,
        organization_id=organization_id,
        warehouse_id=warehouse_id,
        id_type = 'sku',
        period=period,
        length_merge=length_merge,
        date_start = date_start,
        date_end = date_end,
        isIntelligent=False,
        forecast_model='WMA', 
        evaluation='RMSE'  
        )
    # dfp.get_last_predicted_error()
    list_result=dfp.prediction()

    #####################################################
    endtime = datetime.datetime.now()
    print((endtime - starttime),"time used!!!") #0:00:00.280797