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
# 导入自定义的包
from base.base_module import BaseModel
from algorithm.demand_forecast.demand_forecast_algorithm import *

class PrepareDataSerive():
    def __init__(self):
        pass   

    # 根据warehouse_list获取store_id_list
    def get_store_id_list_by_warehouse_ids(self,warehouse_id_list=None):
        # 若为总仓, 则获取所有门店的数据
        # 若为地区仓, 则获取改该地区仓下的所有门店数据
        # ios_base_store
        if len(warehouse_id_list)==1:
            warehouse_id_list_2sql='({})'.format(warehouse_id_list[0])
        else:
            warehouse_id_list_2sql='{}'.format(tuple(warehouse_id_list))
        sql='''
            SELECT *
            FROM ios_base_store
            WHERE warehouse_id in {}
            '''.format(warehouse_id_list_2sql)
        stores = BaseModel.raw(sql)
        if not stores:
            return None
        store_id_list = [store.store_id for store in stores]
        return store_id_list # 返回门店列表,比如:[2,1]

    # 根据设置, 获取要预测的天数
    def get_days_by_forecast_period_range(self,forecast_period_range_id, period, length_merge):
        # 预测周期合并区间  1: 订货周期, 2: 订货批量 3: 天 4:周 5:月 6: 季度
        # 目前只有3, 4
        if forecast_period_range_id == 1:
            # 预测天数为订货周期
            pass
        elif forecast_period_range_id == 2:
            # 预测天数为订货批量
            pass
        elif forecast_period_range_id == 3:
            # 预测天数为天
            days = period * length_merge * 1
        elif forecast_period_range_id == 4:
            # 预测天数为周
            days = period * length_merge * 7
        elif forecast_period_range_id == 5:
            # 预测天数为月
            pass
        else:  # forecast_period_range_id == 6:
            # 预测天数为季度
            pass
        return days

    # 根据参数要求, 时间相关的配置数据
    def get_time_data_from_work_calendar(self):
        sql='''
            SELECT
            work_day AS date,
            holiday_type AS holiday,
            month AS season,
            is_weekend AS weekend
            FROM 
            ios_base_work_calendar
            '''
        sql_results = BaseModel.raw(sql)
        time_data = []
        for result in sql_results:
            data_dict = dict()
            data_dict['date'] = str(result.date)
            data_dict['holiday'] = str(result.holiday)
            data_dict['season'] = str(result.season)
            data_dict['weekend'] = int(result.weekend)
            time_data.append(data_dict)
        # 转成json字符串
        time_data_str=str(time_data)
        return time_data_str

    # 根据参数要求, 获取商品的上市时间
    def get_time2market_data_for_demand_forecast(self,calculate_dimension_id=None,forecast_by='store_id',id=None):
        '''
        按门店或仓库进行预测
        forecast_by='store_id' or forecast_by='warehouse_id'
        output:
        time2market--dict
        '''
        time2market = None
        sql=''
        # 按门店进行预测
        if forecast_by=='store_id':
            if calculate_dimension_id==1: # 按照sku的方式合并
                sql='''
                    SELECT 
                    DISTINCT sku_id AS id,
                    book_date
                    FROM ios_sale_up_to_new
                    WHERE store_id={}
                    '''.format(id)
            elif calculate_dimension_id==2: # 按照skc的方式合并
                sql='''
                    SELECT 
                    DISTINCT skc_id AS id,
                    book_date
                    FROM ios_sale_up_to_new
                    WHERE store_id={}
                    '''.format(id)
            elif calculate_dimension_id==3: # 按照product的方式合并
                sql='''
                    SELECT 
                    DISTINCT product_id AS id,
                    book_date
                    FROM ios_sale_up_to_new
                    WHERE store_id={}
                    '''.format(id)
        # 按仓库进行预测
        elif forecast_by=='warehouse_id':
            if calculate_dimension_id==1: # 按照sku的方式合并
                sql='''
                    SELECT 
                    DISTINCT sku_id AS id,
                    book_date
                    FROM ios_sale_up_to_new
                    WHERE warehouse_id={}
                    '''.format(id)
            elif calculate_dimension_id==2: # 按照skc的方式合并
                sql='''
                    SELECT 
                    DISTINCT skc_id AS id,
                    book_date
                    FROM ios_sale_up_to_new
                    WHERE warehouse_id={}
                    '''.format(id)
            elif calculate_dimension_id==3: # 按照product的方式合并
                sql='''
                    SELECT 
                    DISTINCT product_id AS id,
                    book_date
                    FROM ios_sale_up_to_new
                    WHERE warehouse_id={}
                    '''.format(id)
        else:
            pass
        if sql!='':
            sql_results = BaseModel.raw(sql)
            time2market= dict()
            for result in sql_results:
                time2market[str(result.id)] = str(result.book_date)
        return time2market

    # 获取所有的历史数据
    def get_history_data_for_demand_forecast(self,date_start=None, date_end=None, store_id_list=None, calculate_dimension_id=None, calculate_range_id=None):
        """
        获取所有指定时间的历史数据
        date_start, date_end: 时间, 限定ios_sale_order的sale_date 
        store_id_list: 指定门店, 限定ios_sale_order的store
        calculate_dimension_id: 指定计算维度, 影响ios_sale_order_line的group by方式  # 1.sku合并  2.skc合并  3.product合并
        calculate_range_id: 指定计算范围, 限定sku数量  # 1:全部, 2:快流件 3: 慢流件
        """
        results = None
        if len(store_id_list)==1:
            store_id_list_2sql='({})'.format(store_id_list[0])
        else:
            store_id_list_2sql='{}'.format(tuple(store_id_list))
        if calculate_dimension_id==1: # 按照sku的方式合并
            results = BaseModel.raw("""
                            SELECT
                            ol.sku_id AS id,
                            AVG(ol.amount/ol.quantity) AS fact_price,
                            AVG(ol.price) AS tag_price,
                            AVG(ol.discount/ol.quantity) AS discount,
                            SUM(ol.quantity) AS quantity,
                            product.name AS product_name,
                            sku.bar_code AS bar_code,
                            o.sale_date AS sale_date,
                            oc.classfication_level AS classification_level
                            FROM ios_sale_order_line AS ol
                            INNER JOIN ios_optimization_classificaition AS oc
                            ON ol.sku_id = oc.sku_id
                            INNER JOIN ios_sale_order AS o
                            ON ol.order_id = o.order_id
                            INNER JOIN ios_base_sku AS sku
                            ON ol.product_id = sku.product_id
                            INNER JOIN ios_base_product AS product
                            ON sku.product_id = product.product_id
                            WHERE oc.classfication_level IS NOT NULL AND
                            o.sale_date>='{0}' AND
                            o.sale_date<='{1}' AND
                            o.store_id in {2}
                            GROUP BY ol.sku_id,o.sale_date, oc.classfication_level, sku.bar_code, product.name
                            ORDER BY oc.classfication_level, ol.sku_id;
            """.format(date_start,date_end,store_id_list_2sql))

        elif calculate_dimension_id==2:  # 按照skc的方式合并
            results = BaseModel.raw("""
                            SELECT
                            ol.skc_id AS id,
                            AVG(ol.amount/ol.quantity) AS fact_price,
                            AVG(ol.price) AS tag_price,
                            AVG(ol.discount/ol.quantity) AS discount,
                            SUM(ol.quantity) AS quantity,
                            product.name AS product_name,
                            sku.bar_code AS bar_code,
                            o.sale_date AS sale_date,
                            oc.classfication_level AS classification_level
                            FROM ios_sale_order_line AS ol
                            INNER JOIN ios_optimization_classificaition AS oc
                            ON ol.sku_id = oc.sku_id
                            INNER JOIN ios_sale_order AS o
                            ON ol.order_id = o.order_id
                            INNER JOIN ios_base_sku AS sku
                            ON ol.product_id = sku.product_id
                            INNER JOIN ios_base_product AS product
                            ON sku.product_id = product.product_id
                            WHERE oc.classfication_level IS NOT NULL AND
                            o.sale_date>='{0}' AND
                            o.sale_date<='{1}' AND
                            o.store_id in {2}
                            GROUP BY ol.skc_id,o.sale_date, oc.classfication_level, sku.bar_code, product.name
                            ORDER BY oc.classfication_level, ol.skc_id;
            """.format(date_start,date_end,store_id_list_2sql))

        else:  # calculate_dimension_id==3 按照product的方式合并
            results = BaseModel.raw("""
                            SELECT
                            ol.product_id AS id,
                            AVG(ol.amount/ol.quantity) AS fact_price,
                            AVG(ol.price) AS tag_price,
                            AVG(ol.discount/ol.quantity) AS discount,
                            SUM(ol.quantity) AS quantity,
                            product.name AS product_name,
                            sku.bar_code AS bar_code,
                            o.sale_date AS sale_date,
                            oc.classfication_level AS classification_level
                            FROM ios_sale_order_line AS ol
                            INNER JOIN ios_optimization_classificaition AS oc
                            ON ol.sku_id = oc.sku_id
                            INNER JOIN ios_sale_order AS o
                            ON ol.order_id = o.order_id
                            INNER JOIN ios_base_sku AS sku
                            ON ol.product_id = sku.product_id
                            INNER JOIN ios_base_product AS product
                            ON sku.product_id = product.product_id
                            WHERE oc.classfication_level IS NOT NULL AND
                            o.sale_date>='{0}' AND
                            o.sale_date<='{1}' AND
                            o.store_id in {2} 
                            AND oc.classfication_level>=1
                            AND oc.classfication_level<=2
                            GROUP BY ol.product_id,o.sale_date, oc.classfication_level, sku.bar_code, product.name
                            ORDER BY oc.classfication_level, ol.product_id;
            """.format(date_start,date_end,store_id_list_2sql))
        return results

    # 获取所有的预测数据
    def get_forecast_data_for_demand_forecast(self,date_start, date_end, store_id_list, calculate_dimension_id, calculate_range_id):
        """
        获取所有id对应的商品的预测数据
        date_start, date_end: 时间, 限定ios_sale_order的sale_date  # date_end限定为昨天
        store_id_list: 指定门店, 限定ios_sale_order的store
        calculate_dimension_id: 指定计算维度, 影响ios_sale_order_line的group by方式  # 1.sku合并  2.skc合并  3.product合并
        calculate_range_id: 指定计算范围, 限定sku数量  # 1:全部, 2:快流件 3: 慢流件
        """
        # date_end = str(datetime.datetime.now()-datetime.timedelta(days=1))[0:10]  # 默认为昨天
        results = None
        if len(store_id_list)==1:
            store_id_list_2sql='({})'.format(store_id_list[0])
        else:
            store_id_list_2sql='{}'.format(tuple(store_id_list))
        if calculate_dimension_id==1: # 按照sku的方式合并
            results = BaseModel.raw("""
                                SELECT
                                id,
                                fact_price,
                                tag_price,
                                discount
                                FROM
                                (SELECT
                                ol.sku_id AS id,
                                AVG(ol.amount/ol.quantity) AS fact_price,
                                AVG(ol.price) AS tag_price,
                                AVG(ol.discount/ol.quantity) AS discount,
                                SUM(ol.quantity) AS quantity,
                                product.name AS product_name,
                                sku.bar_code AS bar_code,
                                o.sale_date AS sale_date,
                                oc.classfication_level AS classification_level,
                                row_number() over(partition by ol.sku_id ORDER BY o.sale_date DESC) AS rank
                                FROM ios_sale_order_line AS ol
                                INNER JOIN ios_optimization_classificaition AS oc
                                ON ol.sku_id = oc.sku_id
                                INNER JOIN ios_sale_order AS o
                                ON ol.order_id = o.order_id
                                INNER JOIN ios_base_sku AS sku
                                ON ol.product_id = sku.product_id
                                INNER JOIN ios_base_product AS product
                                ON sku.product_id = product.product_id
                                WHERE oc.classfication_level IS NOT NULL AND
                                o.sale_date>='{0}' AND
                                o.sale_date<='{1}' AND
                                o.store_id in {2}
                                GROUP BY ol.sku_id,o.sale_date, oc.classfication_level, sku.bar_code, product.name
                                ) t
                                WHERE rank=1;
            """.format(date_start,date_end,store_id_list_2sql))

        elif calculate_dimension_id==2:  # 按照skc的方式合并
             results = BaseModel.raw("""
                                SELECT
                                id,
                                fact_price,
                                tag_price,
                                discount
                                FROM
                                (SELECT
                                ol.skc_id AS id,
                                AVG(ol.amount/ol.quantity) AS fact_price,
                                AVG(ol.price) AS tag_price,
                                AVG(ol.discount/ol.quantity) AS discount,
                                SUM(ol.quantity) AS quantity,
                                product.name AS product_name,
                                sku.bar_code AS bar_code,
                                o.sale_date AS sale_date,
                                oc.classfication_level AS classification_level,
                                row_number() over(partition by ol.skc_id ORDER BY o.sale_date DESC) AS rank
                                FROM ios_sale_order_line AS ol
                                INNER JOIN ios_optimization_classificaition AS oc
                                ON ol.sku_id = oc.sku_id
                                INNER JOIN ios_sale_order AS o
                                ON ol.order_id = o.order_id
                                INNER JOIN ios_base_sku AS sku
                                ON ol.product_id = sku.product_id
                                INNER JOIN ios_base_product AS product
                                ON sku.product_id = product.product_id
                                WHERE oc.classfication_level IS NOT NULL AND
                                o.sale_date>='{0}' AND
                                o.sale_date<='{1}' AND
                                o.store_id in {2}
                                GROUP BY ol.skc_id,o.sale_date, oc.classfication_level, sku.bar_code, product.name
                                ) t
                                WHERE rank=1;
            """.format(date_start,date_end,store_id_list_2sql))

        else:  # calculate_dimension_id==3 按照product的方式合并
            results = BaseModel.raw("""
                                SELECT
                                id,
                                fact_price,
                                tag_price,
                                discount
                                FROM
                                (SELECT
                                ol.product_id AS id,
                                AVG(ol.amount/ol.quantity) AS fact_price,
                                AVG(ol.price) AS tag_price,
                                AVG(ol.discount/ol.quantity) AS discount,
                                SUM(ol.quantity) AS quantity,
                                product.name AS product_name,
                                sku.bar_code AS bar_code,
                                o.sale_date AS sale_date,
                                oc.classfication_level AS classification_level,
                                row_number() over(partition by ol.product_id ORDER BY o.sale_date DESC) AS rank
                                FROM ios_sale_order_line AS ol
                                INNER JOIN ios_optimization_classificaition AS oc
                                ON ol.sku_id = oc.sku_id
                                INNER JOIN ios_sale_order AS o
                                ON ol.order_id = o.order_id
                                INNER JOIN ios_base_sku AS sku
                                ON ol.product_id = sku.product_id
                                INNER JOIN ios_base_product AS product
                                ON sku.product_id = product.product_id
                                WHERE oc.classfication_level IS NOT NULL AND
                                o.sale_date>='{0}' AND
                                o.sale_date<='{1}' AND
                                o.store_id in {2}
                                AND oc.classfication_level>=1
                                AND oc.classfication_level<=2
                                GROUP BY ol.product_id,o.sale_date, oc.classfication_level, sku.bar_code, product.name
                                ) t
                                WHERE rank=1;
            """.format(date_start,date_end,store_id_list_2sql))
        return results


    # 根据参数要求, 获取计算用数据.
    def get_history_and_forecast_data_for_demand_forecast(self,forecast_days=None, date_start=None, date_end=None, store_id_list=None, calculate_dimension_id=None, calculate_range_id=None):
        """
          获取所有指定时间的历史数据, 指定预测天数的预测数据(价格取商品价格),
          date_start, date_end: 时间限定ios_sale_order的sale_date  # date_end限定为昨天
          warehouse_id_list: 指定仓库限定ios_sale_order的store
          calculate_dimension_id: 指定计算维度影响ios_sale_order_line的group by方式
          calculate_range_id: 指定计算范围限定sku数量
        """
        input_data = []                 # 传入算法进行计算的数据: 所有id对应的历史数据和预测数据
        date_end=datetime.datetime.strptime(date_end,'%Y-%m-%d')
        # 1. 获取训练数据/历史数据
        train_data = self.get_history_data_for_demand_forecast(date_start, date_end, store_id_list, calculate_dimension_id, calculate_range_id)
        if not train_data:
            print('----所选日期内没有任何数据')
            return None
        for result in train_data:
            data_dict = dict()
            data_dict['id'] = str(result.id)
            data_dict['quantity'] = int(result.quantity)
            data_dict['date'] = str(result.sale_date)[0:10]
            data_dict['tag_price'] = round(float(result.tag_price), 2)
            data_dict['fact_price'] = round(float(result.fact_price), 2)
            data_dict['discount'] = round(float(result.discount), 2)
            data_dict['label'] = 0  # 0表示训练数据
            input_data.append(data_dict)  # ---->> 添加入input_data

        # 2. 获取预测数据.
        forecast_data = self.get_forecast_data_for_demand_forecast(date_start, date_end, store_id_list, calculate_dimension_id, calculate_range_id)
        if not forecast_data:
            print('----所选日期内没有预测数据')
            return None
        for result in forecast_data:
            for i in range(forecast_days):
                data_dict = dict()
                data_dict['id'] = str(result.id)
                data_dict['quantity'] = 0  # 预测数据销量为0
                data_dict['date'] = str(date_end + datetime.timedelta(days=i+1))[0:10]
                data_dict['tag_price'] = round(float(result.tag_price), 2)
                data_dict['fact_price'] = round(float(result.fact_price), 2)
                data_dict['discount'] = round(float(result.discount), 2)
                data_dict['label'] = 1  # 表示预测数据
                input_data.append(data_dict)

        input_data_str=str(input_data)
        return input_data_str

class DemandForecastProcess():
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
        id=1                               # 'store_id' or 'warehouse_id'
        ):
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

    def get_data(self):
        '''
        获取销量预测相关的输入数据
        '''
        # 01. 根据warehouse_id_list获取对应的store_id_list
        if self.forecast_by=='store_id': # 按门店预测
            store_id_list=[self.id]
        else:                       # 按仓库预测
            store_id_list = PrepareDataSerive().get_store_id_list_by_warehouse_ids(self.warehouse_id_list)
        # 02. 根据forecast_period_range_id预测周期合并方式+预测周期数+合并区间长度, 判断预测天数
        days = PrepareDataSerive().get_days_by_forecast_period_range(self.forecast_period_range_id, self.period, self.length_merge)
        # 03. 根据参数要求, 获取训练和预测数据
        input_data_str = PrepareDataSerive().get_history_and_forecast_data_for_demand_forecast(days, self.date_start, self.date_end, store_id_list, self.calculate_dimension_id, self.calculate_range_id)
        # 04. 根据参数要求, 时间相关的配置数据
        time_data_str = PrepareDataSerive().get_time_data_from_work_calendar()
        # 05. 根据参数要求, 获取商品的上市时间
        time2market = PrepareDataSerive().get_time2market_data_for_demand_forecast(self.calculate_dimension_id,self.forecast_by,self.id)
        return input_data_str, time_data_str,time2market

    def prediction(self,isIntelligent=None,input_data_str=None,time_data_str=None,time2market=None,forcast_models=['GBRT'],evaluation='MAPE'):
        # 调用销量预测算法 demand_forecast_algorithm
        dfa=DemandForecastAlgorithm(
            isIntelligent=isIntelligent,
            date_start=self.date_start,
            date_end=self.date_end,
            input_data_str=input_data_str,
            time_data_str=time_data_str,
            time2market=time2market,
            forcast_models=forcast_models,
            evaluation=evaluation,
            length_merge=self.length_merge,
            period=self.period)
        json_result=dfa.run()
        return json_result

########################################################################################
# 测试代码
if __name__=='__main__':
    '''
    # (1) 测试PrepareDataSerive类
    pds=PrepareDataSerive()
    store_id_list=pds.get_store_id_list_by_warehouse_ids(warehouse_id_list=[1,2,3])
    print('根据仓库id列表,获取相应的门店id列表为:',store_id_list)

    days=pds.get_days_by_forecast_period_range(forecast_period_range_id=3, period=7, length_merge=1)
    print('根据参数,计算预测天数为:',days)

    time_data_str=pds.get_time_data_from_work_calendar()
    # json字符串转成字典列表
    json_list = demjson.decode(time_data_str)
    print('------时间相关数据--------')
    for x  in json_list[:3]:
        print(x)    

    time2market=pds.get_time2market_data_for_demand_forecast(calculate_dimension_id=3,forecast_by='store_id',id=1)
    print('------产品上市时间--------')
    for k,t2m in enumerate(time2market):
        if k<3:
            print(t2m,time2market[t2m]) 
        else:
            break

    train_data=pds.get_history_data_for_demand_forecast(date_start='2018-01-28', date_end='2018-04-25', store_id_list=[1], calculate_dimension_id=3, calculate_range_id=None)
    print('------训练数据--------')
    for result in train_data[:5]:
        print('id:',str(result.id),'\t',end='')
        print('date:',str(result.sale_date)[0:10],'\t',end='')
        print('quantity:',int(result.quantity),'\t',end='')
        print('tag_price:',round(float(result.tag_price), 2),'\t',end='')
        print('fact_price:',round(float(result.fact_price), 2),'\t',end='')
        print('discount:',round(float(result.discount), 2),'\t',end='')
        print('label:',0)

    predict_data=pds.get_forecast_data_for_demand_forecast(date_start='2018-01-28', date_end='2018-04-25', store_id_list=[1], calculate_dimension_id=3, calculate_range_id=None)
    print('------预测数据--------')
    for result in train_data[:5]:
        print('id:',str(result.id),'\t',end='')
        print('tag_price:',round(float(result.tag_price), 2),'\t',end='')
        print('fact_price:',round(float(result.fact_price), 2),'\t',end='')
        print('discount:',round(float(result.discount), 2),'\t',end='')
        print('label:',1)

    input_data_str=pds.get_history_and_forecast_data_for_demand_forecast(forecast_days=days, date_start='2018-01-28', date_end='2018-04-25', store_id_list=[1], calculate_dimension_id=3, calculate_range_id=None)
    # json字符串转成字典列表
    json_list = demjson.decode(input_data_str)
    print('------输入数据--------')
    for x  in json_list[:3]:
        print(x) 

    '''

    # (2) 测试DemandForecastProcess类
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