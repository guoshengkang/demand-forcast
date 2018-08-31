#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-27 12:14:26
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import sys
import pandas as pd
import numpy as np
import datetime
import time
sys.path.append('../')

from base.base_module import BaseModel
from model.optimization.forecast import ProductFeature

class CollectFeatureDataProcess():
	'''
	定义获取产品在某一天的特征数据的函数
	(1) 查找产品在某一天的销售价格 get_sale_price()
	(2) 查找产品在某一天的采购价 get_purchase_price()
	(3) 查找产品在某一天的销量 get_sale_quantity()
	(4) 查找产品在某一天的促销情况 get_promotion()
	(5) 查找产品在某一天的状态 get_product_status()
	(6) 查找产品在某一天的库存 get_on_hand_quantity()
	(7) 获取产品在某一段日期内的特征数据并写入数据库 feature_data_aggregation() 调用:(1)-(2)-(3)-(4)-(5)-(6)
	(8) 获取某一仓库下门店,并将门店的产品在某一段日期内的特征数据并写入数据库collect_feature_data() 调用:(7)
	(9) run(),调用:(8)
	'''
	def __init__(self,warehouse_id=1,
		id_type='sku',
		start_date='2018-01-01',
		end_date='2018-05-02'):
		self.warehouse_id=warehouse_id
		self.id_type=id_type
		self.start_date=start_date
		self.end_date=end_date

	# (1) 查找产品在某一天的销售价格
	def get_sale_price(self,warehouse_id=None,store_id=None,id=None,id_type='sku',book_date=None):
		"""
		从 ios_base_price_change 表中获取产品在某一天的销售价
		"""
		sql="""
		SELECT
		new_sale_price
		FROM ios_base_price_change
		WHERE store_id={0}
		AND start_date<='{1}' AND end_date>='{1}'
		AND {2}_id={3}
		""".format(store_id,book_date,id_type,id)
		# print(sql)
		rows = BaseModel.raw(sql)
		if len(rows)==1:
			sale_price=round(float(rows[0].new_sale_price), 2)
			res_dict=[{
			'warehouse_id':warehouse_id,
			'store_id':store_id,
			'{}_id'.format(id_type):id,
			'book_date':book_date,
			'feature_name':'sale_price',
			'feature_type':0,
			'feature_value':sale_price
			}]
		else:
			res_dict=None
			if len(rows)==0:
				print('[ERROR]:找不到store_id({3})的{0}_id({1})在{2}的销售价!!!'.format(id_type,id,book_date,store_id))
			if len(rows)>1:
				print('[ERROR]:找到store_id({3})的{0}_id({1})在{2}的多个销售价!!!'.format(id_type,id,book_date,store_id))

		return res_dict

	# (2) 查找产品在某一天的采购价
	def get_purchase_price(self,warehouse_id=1,store_id=None,id=None,id_type='sku',book_date=None):
		"""
		从 ios_base_supplier_product 表中获取产品在某一天的采购价
		"""
		sql="""
		SELECT
		purchase_price
		FROM ios_base_supplier_product_relation
		WHERE start_date<='{0}' AND end_date>='{0}'
		AND {1}_id={2}
		""".format(book_date,id_type,id)
		# print(sql)
		rows = BaseModel.raw(sql)
		if len(rows)==1:
			purchase_price=round(float(rows[0].purchase_price), 2)
			res_dict=[{
			'warehouse_id':warehouse_id,
			'store_id':store_id,
			'{}_id'.format(id_type):id,
			'book_date':book_date,
			'feature_name':'purchase_price',
			'feature_type':0,
			'feature_value':purchase_price
			}]
		else:
			res_dict=None
			if len(rows)==0:
				print('[ERROR]:找不到store_id({3})的{0}_id({1})在{2}的采购价!!!'.format(id_type,id,book_date,store_id))
			if len(rows)>1:
				print('[ERROR]:找到store_id({3})的{0}_id({1})在{2}的多个采购价!!!'.format(id_type,id,book_date,store_id))

		return res_dict

	# (3) 查找产品在某一天的销量
	def get_sale_quantity(self,warehouse_id=1,store_id=None,id=None,id_type='sku',book_date=None):
		"""
		从 ios_sale_order 和 ios_sale_order_line 表中获取产品在某一天的销量
		"""
		sql="""
		SELECT
		ol.{2}_id AS id,
		SUM(ol.quantity) AS quantity
		FROM ios_sale_order AS o
		INNER JOIN ios_sale_order_line AS ol
		ON o.order_id=ol.order_id
		INNER JOIN ios_base_store AS s
		ON s.store_id=o.store_id
		WHERE o.store_id={0} AND o.sale_date='{1}' AND ol.{2}_id={3}
		AND o.status=1 
		AND ol.status=1
		AND ol.quantity>0
		GROUP BY ol.{2}_id
		""".format(store_id,book_date,id_type,id)
		# print(sql)
		rows = BaseModel.raw(sql)
		if len(rows)==1:
			quantity=round(float(rows[0].quantity), 2) 
		else:
			# print('[INFO]:找不到store_id({3})的{0}_id({1})在{2}的销量信息!!!'.format(id_type,id,book_date,store_id))
			quantity=0
		res_dict=[{
		'warehouse_id':warehouse_id,
		'store_id':store_id,
		'{}_id'.format(id_type):id,
		'book_date':book_date,
		'feature_name':'quantity',
		'feature_type':0,
		'feature_value':quantity
		}]
		return res_dict

	# (4) 查找产品在某一天的促销情况
	def get_promotion(self,warehouse_id=1,store_id=None,id=None,id_type='sku',book_date=None):
		"""
		从 ios_base_supplier_product 表中获取产品在某一天的促销情况
		"""
		sql="""
		SELECT
		spp.type
		FROM ios_sale_promotion AS sp
		INNER JOIN ios_sale_promotion_policy AS spp
		ON sp.policy_id=spp.policy_id
		WHERE sp.store_id={0} AND sp.{2}_id={3}
		AND spp.start_time<='{1}' AND spp.end_time>='{1}'
		""".format(store_id,book_date,id_type,id)
		# print(sql)
		rows = BaseModel.raw(sql)
		if len(rows)>=1:
			types=[int(row.type) for row in rows]
			res_dict=[]
			for promotion_type in types:
				tmp_dict={
				'warehouse_id':warehouse_id,
				'store_id':store_id,
				'{}_id'.format(id_type):id,
				'book_date':book_date,
				'feature_name':'promotion',
				'feature_type':promotion_type,
				'feature_value':1
				}
				res_dict.append(tmp_dict)
		else:
			res_dict=None
			print('[INFO]:找不到store_id({3})的{0}_id({1})在{2}的促销信息!!!'.format(id_type,id,book_date,store_id))
		return res_dict

	# (5) 查找产品在某一天的状态:新品-正常-淘汰-缺货
	def get_product_status(self,warehouse_id=1,store_id=None,id=None,id_type='sku',book_date=None):
		"""
		从 ios_base_supplier_product 表中获取产品在某一天的采购价
		"""
		sql="""
		SELECT
		product_status
		FROM
			(SELECT
			stage AS product_status,
			row_number() over(partition by {1}_id ORDER BY book_date DESC) AS rank
			FROM ios_base_product_classification
			WHERE booK_date<='{0}' AND {1}_id={2}
			) AS t
		WHERE rank=1
		""".format(book_date,id_type,id)
		# print(sql)
		rows = BaseModel.raw(sql)
		if len(rows)==1:
			product_status=int(rows[0].product_status)
			res_dict=[{
			'warehouse_id':warehouse_id,
			'store_id':store_id,
			'{}_id'.format(id_type):id,
			'book_date':book_date,
			'feature_name':'product_status',
			'feature_type':product_status,
			'feature_value':1
			}]
		else:
			res_dict=None
			print('[ERROR]:找不到store_id({3})的{0}_id({1})在{2}的产品状态信息!!!'.format(id_type,id,book_date,store_id))
		return res_dict

	# (6) 查找产品在某一天的库存
	def get_on_hand_quantity(self,warehouse_id=1,store_id=None,id=None,id_type='sku',book_date=None):
		"""
		从 ios_base_supplier_product 表中获取产品在某一天的库存:0-无库存,1-有库存
		"""
		sql="""
		SELECT
		stock_on_hand.{2}_id AS id,
		stock_on_hand.on_hand_quantity AS on_hand_quantity,
		Date(stock_on_hand.book_date) AS book_date,
		row_number() over(partition by stock_on_hand.{2}_id ORDER BY stock_on_hand.book_date DESC) AS rank
		FROM ios_stock_on_hand AS stock_on_hand
		INNER JOIN ios_base_warehouse_location  AS warehouse_location
		ON warehouse_location.location_id = stock_on_hand.location_id
		INNER JOIN ios_base_warehouse AS warehouse
		ON warehouse.warehouse_id = warehouse_location.warehouse_id
		INNER JOIN ios_base_store AS store
		ON store.warehouse_id = warehouse.warehouse_id
		WHERE 
		store.store_id = {0} 
		AND warehouse_location.location_type=1 
		AND stock_on_hand.{2}_id={3}
		AND stock_on_hand.book_date<='{1}'
		limit 1
		""".format(store_id,book_date,id_type,id)
		# print(sql)
		rows = BaseModel.raw(sql)
		if len(rows)==1:
			on_hand_quantity=1 if int(rows[0].on_hand_quantity)>0 else 0
			res_dict=[{
			'warehouse_id':warehouse_id,
			'store_id':store_id,
			'{}_id'.format(id_type):id,
			'book_date':book_date,
			'feature_name':'on_hand_quantity',
			'feature_type':0,
			'feature_value':on_hand_quantity
			}]
		else:
			res_dict=None
			print('[ERROR]:找不到store_id({3})的{0}_id({1})在{2}的产品库存信息!!!'.format(id_type,id,book_date,store_id))
		return res_dict

	# (7) 获取产品在某一段日期内的特征数据并写入数据库,调用:(1)-(2)-(3)-(4)-(5)-(6)
	def feature_data_aggregation(self,warehouse_id=1,store_id=1,id=None,id_type='sku',start_date=None,end_date=None):
		'''
		将warehouse_id和store_id中sku_id在start_date和end_date日期范围内的所有特征数据写入数据库
		'''
		all_dates=pd.date_range(start=start_date,end=end_date,freq='d')
		insert_values=[]
		for one_day in all_dates:
			sale_price=self.get_sale_price(warehouse_id=warehouse_id,store_id=store_id,id=id,id_type=id_type,book_date=str(one_day)[:10])
			purchase_price=self.get_purchase_price(warehouse_id=warehouse_id,store_id=store_id,id=id,id_type=id_type,book_date=str(one_day)[:10])
			quantity=self.get_sale_quantity(warehouse_id=warehouse_id,store_id=store_id,id=id,id_type=id_type,book_date=str(one_day)[:10])
			promotion=self.get_promotion(warehouse_id=warehouse_id,store_id=store_id,id=id,id_type=id_type,book_date=str(one_day)[:10])
			product_status=self.get_product_status(warehouse_id=warehouse_id,store_id=store_id,id=id,id_type=id_type,book_date=str(one_day)[:10])
			on_hand_quantity=self.get_on_hand_quantity(warehouse_id=warehouse_id,store_id=store_id,id=id,id_type=id_type,book_date=str(one_day)[:10])
			if sale_price:
				insert_values.extend(sale_price)
			if purchase_price:
				insert_values.extend(purchase_price)
			if quantity:
				insert_values.extend(quantity)
			if promotion:
				insert_values.extend(promotion)
			if product_status:
				insert_values.extend(product_status)
			if on_hand_quantity:
				insert_values.extend(on_hand_quantity)
		# !!! 调式时,建议不操作数据库
		# 先删除数据
		# if id_type=='sku':
		# 	ProductFeature.delete().where((ProductFeature.warehouse_id==1) 
		# 		& (ProductFeature.store_id==1) 
		# 		& (ProductFeature.sku_id==id) 
		# 		& (ProductFeature.book_date>=start_date) 
		# 		& (ProductFeature.book_date<=end_date)).execute()
		# elif id_type=='skc':
		# 	ProductFeature.delete().where((ProductFeature.warehouse_id==1) 
		# 		& (ProductFeature.store_id==1) 
		# 		& (ProductFeature.skc_id==id) 
		# 		& (ProductFeature.book_date>=start_date) 
		# 		& (ProductFeature.book_date<=end_date)).execute()
		# else:
		# 		ProductFeature.delete().where((ProductFeature.warehouse_id==1) 
		# 		& (ProductFeature.store_id==1) 
		# 		& (ProductFeature.product_id==id) 
		# 		& (ProductFeature.book_date>=start_date) 
		# 		& (ProductFeature.book_date<=end_date)).execute()
		# 将sku_id的的特征数据写入数据库
		# ProductFeature.insert_many(insert_values).execute()

	# (8) 获取某一仓库下门店,并将门店的产品在某一段日期内的特征数据并写入数据库,调用:(7)
	def collect_feature_data(self,warehouse_id=1,id_type='sku',start_date='2018-01-01',end_date='2018-05-02'):
		'''
		将warehouse_id中所有store_id下的sku_id在日期范围内容的特征数据查找出来并写入数据库
		'''
		# (step 1) 查找warehouse_id下的所有store_id
		sql="""
			SELECT *
			FROM ios_base_store
			WHERE warehouse_id={}
			""".format(warehouse_id)
		rows = BaseModel.raw(sql)
		store_id_list = [row.store_id for row in rows]
		print("[INFO]:找到warehouse_id({0})下的{1}个store_id:{2}".format(warehouse_id,len(store_id_list),store_id_list))

		# (step 2) 查找store_id下的所有sku_id及上新日期
		for store_rank,store_id in enumerate(store_id_list):
			sql="""
				SELECT 
				DISTINCT
				{0}_id, 
				book_date
				FROM ios_sale_up_to_new
				WHERE warehouse_id={1} 
				AND store_id={2}
				-- AND sku_id=13689
				limit 5
				""".format(id_type,warehouse_id,store_id)
			rows = BaseModel.raw(sql)

		# (step 3) 查找store_id下的所有sku_id在日期范围内的特征数据并写入数据库
			# 循环所有sku_id
			for sku_rank,row in enumerate(rows):
				current_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				sku_id=row.sku_id
				print('current_time:%s Processing %d-th sku of %d-th store:%s ... There are %d skus in total ...'%(current_time,sku_rank+1,store_rank+1,sku_id,len(rows)))
				book_date=str(row.book_date) # datetime类型转为字符串类型
				start_date=max(start_date,book_date) 		
				self.feature_data_aggregation(warehouse_id=1,store_id=1,id=sku_id,id_type='sku',start_date=start_date,end_date=end_date)
	# (9) 调用:(8)
	def run(self):
		# 调用 collect_feature_data()
		self.collect_feature_data(warehouse_id=self.warehouse_id,id_type=self.id_type,start_date=self.start_date,end_date=self.end_date)

########################################################################################
# '''
# 类测试代码
if __name__=='__main__':
	# 删除数据
	# ProductFeature.delete().where((ProductFeature.warehouse_id==1) 
	# 	& (ProductFeature.store_id==1) 
	# 	& (ProductFeature.book_date>='2018-01-01') 
	# 	& (ProductFeature.book_date<='2018-05-02')).execute()

	# 参数输入
	cfdp=CollectFeatureDataProcess(warehouse_id=1,id_type='sku',start_date='2018-01-01',end_date='2018-05-02')
	cfdp.run()
# '''
########################################################################################
'''
# 类方法单元测试代码
if __name__=='__main__':
	insert_values=[]
	cfdp=CollectFeatureDataProcess(warehouse_id=1,id_type='sku',start_date='2018-01-01',end_date='2018-05-02')

	# 测试 get_sale_price
	sale_price=cfdp.get_sale_price(warehouse_id=1,store_id=1,id=10239,id_type='sku',book_date='2018-05-10')
	print('sale_price:',sale_price)
	
	# 测试 get_purchase_price
	purchase_price=cfdp.get_purchase_price(warehouse_id=1,store_id=1,id=10239,id_type='sku',book_date='2018-05-24')
	print('purchase_price:',purchase_price)
	
	# 测试 get_sale_quantity
	quantity=cfdp.get_sale_quantity(warehouse_id=1,store_id=1,id=44117,id_type='sku',book_date='2018-05-24')
	print('quantity:',quantity)	

	# 测试 get_promotion
	promotion=cfdp.get_promotion(warehouse_id=1,store_id=1,id=10239,id_type='sku',book_date='2018-05-14')
	print('promotion:',promotion)
	
	# 测试 get_product_status
	product_status=cfdp.get_product_status(warehouse_id=1,store_id=1,id=11856,id_type='sku',book_date='2018-02-01')
	print('product_status:',product_status)
	
	# 测试 get_on_hand_quantity
	on_hand_quantity=cfdp.get_on_hand_quantity(warehouse_id=1,store_id=1,id=14157,id_type='sku',book_date='2018-04-15')
	print('on_hand_quantity:',on_hand_quantity)

	print('-'*30)
	# None 类型不能被list extend
	if sale_price:
		insert_values.extend(sale_price)
	if purchase_price:
		insert_values.extend(purchase_price)
	if quantity:
		insert_values.extend(quantity)
	if promotion:
		insert_values.extend(promotion)
	if product_status:
		insert_values.extend(product_status)
	if on_hand_quantity:
		insert_values.extend(on_hand_quantity)

	# print(insert_values)
	# # 单条记录插入 字典或字典列表
	# # ProductFeature.insert(insert_values).execute()
	# # 多条记录插入
	# ProductFeature.insert_many(insert_values).execute()
'''

