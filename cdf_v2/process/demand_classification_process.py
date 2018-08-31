#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-31 17:04:32
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})
# 测试代码时使用
import sys
sys.path.append('../')

import os
import pandas as pd
import numpy as np
import datetime
# 导入自定义包
from base.base_module import BaseModel,db
from model.optimization.forecast import DemandClassification
from algorithm.demand_forecast.feature_engineering import timeseries_merge

# 参考资料
# http://www.supplychainforum.com/showthread.php/2283-average-inter-demand-interval
# https://frepple.com/blog/demand-classification/

class CalculateDemandClassification():
	'''
	计算ADI值和CV²以及销量的类别
	'''
	def __init__(self,tmp_list=[],sku_id=None,length_merge=1):
		# self.tmp_list=tmp_list
		# 按length_merge天合并
		self.tmp_list=timeseries_merge(tmp_list,length_merge=length_merge)
		# 计算有销量的天数
		self.sale_days=sum(np.array(tmp_list)>0)
		self.adi_value=None
		self.cv2_value=None
		self.demand_class=0
		self.sku_id=sku_id
		self.needed_sale_days=10
		# print(self.tmp_list)

	'''
	Average Demand Interval
	'''
	def ADI(self):
		intervals=[]
		previous=0
		for index in range(1,len(self.tmp_list)):
			if self.tmp_list[index]>0:
				current=index
				intervals.append(current-previous)
				previous=current
		if len(intervals)>0:
			self.adi_value=sum(intervals)/len(intervals)
			# 保留2位小数
			self.adi_value=np.round(self.adi_value,2)
	'''
	square of the Coefficient of Variation
	'''
	def CV(self):
		if self.sale_days>0: # 销量不全部为0
			tmp_array=np.array(self.tmp_list)
			non_zeros=tmp_array[tmp_array>0]
			cv=np.std(non_zeros)/np.mean(non_zeros)
			self.cv2_value=cv**2
			# 保留2为小数
			self.cv2_value=np.round(self.cv2_value,2)

	def fit(self):
		try:
			self.ADI()
		except Exception as e:
			print('[INFO]:failed to calculate ADI value when processing sku_id:%s (because %s)'%(self.sku_id,e))
		try:
			self.CV()
		except Exception as e:
			print('[INFO]:failed to calculate cv2 value (%s)'%e)
		# 有销量的值>=10天才计算其类别
		if self.sale_days>=self.needed_sale_days:
			if self.adi_value and self.cv2_value:
				if (self.adi_value  < 1.32 and self.cv2_value  < 0.49):
					self.demand_class=1 # 'smooth'
				elif (self.adi_value >= 1.32 and self.cv2_value < 0.49):
					self.demand_class=2 # 'intermittent'
				elif (self.adi_value < 1.32 and self.cv2_value >= 0.49):
					self.demand_class=3 # 'erratic'
				else: # (self.adi_value >= 1.32 and self.cv2_value >= 0.49)
					self.demand_class=4 # 'lumpy'

class DemandClassificationProcess():
	'''
	计算某个warehouse_id下面sku_id的销量分类,并将结果写入 ios_optimization_demand_classification
	'''
	def __init__(self,warehouse_id=1,start_date='2018-01-28',end_date='2018-05-02',use_recent_days=None,length_merge=1):
		'''
		warehouse_id:获取数据的仓库id
		start_date:获取数据的开始日期
		end_date:获取数据的结束日期
		use_recent_days:分类使用最近的数据天数,默认为None(即使用全部数据)
		length_merge:数据的合并天数
		'''
		self.warehouse_id=warehouse_id
		self.start_date=start_date
		self.end_date=end_date
		self.use_recent_days=use_recent_days
		self.length_merge=length_merge
		print('[INFO]:{:=^50}'.format(' start '))

	def run(self):
		print('[INFO]:{:-^30}'.format('开始计算仓库(%d)的需求分类'%self.warehouse_id))

		# (1) 获取产品的上市时间
		sql='''
		    SELECT 
		    DISTINCT sku_id AS id,
		    DATE(book_date) AS book_date
		    FROM ios_sale_up_to_new
		    WHERE warehouse_id={}
		    '''.format(self.warehouse_id)
		sql_results = BaseModel.raw(sql)
		time2market= dict()
		# for result in sql_results:
		# 	time2market[str(result.id)] = str(result.book_date)
		print('[INFO]:{:-^30}'.format('完成获取产品上市时间'))

		# (2) 获取销量数据
		sql="""
		SELECT
		ol.sku_id AS id,
		DATE(o.sale_date) AS book_date,
		SUM(ol.quantity) AS quantity
		FROM ios_sale_order AS o
		INNER JOIN ios_sale_order_line AS ol
		ON o.order_id=ol.order_id
		INNER JOIN ios_base_store AS s
		ON o.store_id=s.store_id
		WHERE s.warehouse_id={0} 
		AND o.sale_date>='{1}'
		AND o.sale_date<='{2}'
		-- AND  ol.sku_id=11516
		GROUP BY ol.sku_id,book_date
		ORDER BY book_date DESC
		""".format(self.warehouse_id,self.start_date,self.end_date)
		input_df=pd.read_sql(sql, db)
		# 将book_date列转成日期类型
		input_df['book_date']=input_df['book_date'].map(lambda x: datetime.datetime.strptime(str(x),'%Y-%m-%d'))
		print('[INFO]:{:-^30}'.format('完成获取产品销量数据'))

		# (3) 计算销量类别
		from_date=datetime.datetime.strptime(self.start_date,'%Y-%m-%d')
		to_date=datetime.datetime.strptime(self.end_date,'%Y-%m-%d')

		insert_values=[]
		df=input_df.drop_duplicates()
		# 所有的产品id
		ids=df['id'].unique()
		if len(ids)==0:
			print("[INFO]:未获取到任何产品的销量数据,请检查输入参数及SQL语句！！！")
			return None
		else:
			print('[INFO]:{:-^30}'.format('获取到%d个产品的销量数据'%len(ids)))
		print('[INFO]:{:-^30}'.format('使用最近%d天的销量数据做需求分类'%self.use_recent_days))
		# 循坏每个id
		for index_no,id in enumerate(ids): 
			# print('Processing %d-th sku %s ... There are %d skus in total ...'%(index_no+1,id,len(ids)))
			df_tmp=df[df['id']==id] # 将id对应的所有数据取出来
			if time2market.get(str(id)):
				# 获取产品上市日期
				date_market=time2market.get(str(id))
				date_market=datetime.datetime.strptime(date_market,'%Y-%m-%d')
				date_min=max(date_market,from_date)
			else: # 未获取到产品的上市日期
				date_min=from_date
			date_max=to_date

			# date_min=datetime.datetime.strptime('2017-01-01','%Y-%m-%d')
			# date_max=datetime.datetime.strptime('2017-12-31','%Y-%m-%d')
			# date_min=datetime.datetime.strptime('2018-01-28','%Y-%m-%d')
			# date_max=datetime.datetime.strptime('2018-05-02','%Y-%m-%d')

			df_date=df_tmp.set_index(['book_date']) # 将date列设置为索引,仍然为DataFrame
			ts_quantity=df_date['quantity'] # 返回Series ******
			dates=pd.date_range(date_min,date_max) # 有效的历史日期
			ts_quantity=ts_quantity.reindex(dates,fill_value=0) # 重新索引 
			ts_quantity=ts_quantity.astype(np.float64) # 将其转化为float64 ******

			# 取最近N天的数据:N=use_recent_days
			if self.use_recent_days:
				ts_quantity=ts_quantity[-self.use_recent_days:]

			dc=CalculateDemandClassification(tmp_list=ts_quantity,sku_id=id,length_merge=self.length_merge)
			dc.fit()
			tmp_dict={
			'warehouse_id':self.warehouse_id,
			'sku_id':id,
			'adi_value':dc.adi_value,
			'cv2_value':dc.cv2_value,
			'demand_class':dc.demand_class,
			'sale_days':dc.sale_days
			}
			insert_values.append(tmp_dict)
		print('[INFO]:{:-^30}'.format('完成计算产品销量类别'))

		# (4) 销量分类结果写入数据库
		# 测试时不操作数据库
		# # 删除warehouse_id下面对应的销量分类数据
		# DemandClassification.delete().where(DemandClassification.warehouse_id==self.warehouse_id).execute()
		# # 多条记录插入
		# DemandClassification.insert_many(insert_values).execute()
		print('[INFO]:{:-^30}'.format('完成将产品销量类别数据写入数据库'))
		print('[INFO]:{:=^50}'.format(' end '))

# 测试代码
if __name__=='__main__':
	DemandClassificationProcess(warehouse_id=1,start_date='2018-01-28',end_date='2018-05-02',use_recent_days=90,length_merge=7).run()
	DemandClassificationProcess(warehouse_id=2,start_date='2017-01-01',end_date='2017-12-31',use_recent_days=90,length_merge=7).run()

'''
# 各类别的统计
SELECT
warehouse_id,
demand_class,
count(1),
avg(sale_days)::INTEGER AS sale_days,
max(sale_days) AS max_sale_days,
min(sale_days) AS min_sale_days
FROM ios_optimization_demand_classification
GROUP BY warehouse_id,demand_class
ORDER BY warehouse_id,demand_class
'''