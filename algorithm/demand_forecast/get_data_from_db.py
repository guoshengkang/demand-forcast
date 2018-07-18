#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-27 17:57:00
# @Auth  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import pandas as pd
from peewee import Model,PostgresqlDatabase
from playhouse.pool import PooledPostgresqlDatabase
import datetime

db = PooledPostgresqlDatabase(database='ios2',
                              host='172.12.78.217',
                              port=5432,
                              user='postgres',
                              password='Password123',
                              max_connections=20,    # 可省略
                              stale_timeout=300,     # 可省略
                             )

class BaseModel(Model):
    class Meta:
        database = db


# sql="""
# 	SELECT
# 	商品编号               AS id,
# 	CAST(销售日期 AS date) AS date,
# 	MAX("售价") 		   AS fact_price,
# 	SUM(销售数量)          AS quantity,
# 	0 AS label,
# 	t1.商品类别 AS class
# 	FROM tmp_bgy_data_from_20160101 t1
# 	INNER JOIN 
# 		(SELECT
# 		商品类别,
# 		count(DISTINCT 商品编号) AS p_num
# 		FROM tmp_bgy_data_from_20160101
# 		GROUP BY 商品类别 HAVING count(DISTINCT 商品编号)>=20
# 		ORDER BY p_num
# 		) t2
# 	ON t1.商品类别=t2.商品类别
# 	INNER JOIN 
# 		(SELECT
# 		id,
# 		count(1) AS days
# 		FROM tmp_bgy_order_data
# 		GROUP BY id HAVING count(1)>=20
# 		) t3
# 	ON t1.商品编号=t3.id	
# 	WHERE "功能号"='1' AND 销售数量>0 AND t1.商品类别='10102'
# 	GROUP BY t1.商品类别,商品编号,CAST(销售日期 AS date)
# 	ORDER BY t1.商品类别,商品编号,CAST(销售日期 AS date)
# 	"""

# sql="""
# 	SELECT
# 	t1.*,
# 	t2.classfication_level AS class,
# 	0 AS label
# 	FROM tmp_kgs_all_data t1
# 	INNER JOIN 
# 		(
# 		SELECT
# 		DISTINCT product_id AS id,
# 		classfication_level
# 		FROM ios_optimization_classificaition
# 		WHERE warehouse_id=1
# 		) t2
# 	ON  t1."id"=t2."id"
# 	WHERE t1."date">='2018-01-01' 
# 	AND t2.classfication_level<=3 
# 	AND t2.classfication_level>0
# 	AND t1."id"=43791
# 	-- AND t1."id"=44156
# 	-- AND (t1."id"=41427 OR t1."id"=41841 OR t1."id"=44156)
# 	ORDER BY class,id,date
# """

# sql="""
#   SELECT 
#   t1.*
#   FROM tmp_kgs_abc_6sku t1
#   WHERE 
#   -- t1."id"=14118 
#    -- t1.id=17185 
#    t1.id=14270 
#    -- t1.id=12391 
#    -- t1.id=13420 
#    -- t1.id=13859
#   """
sql="""
	SELECT 
	t1."id",
	t1."date",
	t1.quantity,
	t1.tag_price,
	t1.fact_price,
	t1.discount/t1.quantity AS discount,
	t4.promotion,
	0 AS label
	FROM tmp_kgs_all_data t1
	-- INNER JOIN tmp_kgs_selected_class6_skus t2
	-- ON t1."id"=t2.id
	INNER JOIN ios_base_product t3
	ON t1."id"=t3.product_id
	LEFT JOIN
		(
		SELECT
		DISTINCT bar_code,promotion_date, 1 AS promotion
		FROM tmp_kgs_promotion
		) t4
	ON t3.bar_code=t4.bar_code AND CONCAT(EXTRACT(YEAR from t1."date"),'-',EXTRACT(MONTH from t1."date"))=t4.promotion_date
	WHERE t1."date">='2018-01-01'
	AND t1."id"=44117
	-- AND (t1."id"=44564 OR t1."id"=44655 OR t1."id"=46873 OR t1."id"=46876)
	ORDER BY "id","date"
	"""

input_data_df=pd.read_sql(sql, db)
# 将date列转成日期类型
input_data_df['date']=input_data_df['date'].map(lambda x: datetime.datetime.strptime(str(x),'%Y-%m-%d'))
print(input_data_df.head())
# print(input_data_df.dtypes) #datetime64

config_sql='''
	SELECT
	work_day AS date,
	holiday_type AS holiday,
	month AS season,
	is_weekend AS weekend
	FROM 
	ios_base_work_calendar
	'''
config_data_df=pd.read_sql(config_sql, db)
# 将date列转成日期类型
config_data_df['date']=config_data_df['date'].map(lambda x: datetime.datetime.strptime(str(x),'%Y-%m-%d'))
# config_data_df['weekend_5']=config_data_df['weekend'].map(lambda x: x+5)

print(config_data_df.head())
print(config_data_df.dtypes) #datetime64