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
                              host='172.12.78.132',
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

# sql="""
# 	SELECT 
# 	t1."id",
# 	t1."date",
# 	t1.quantity,
# 	t1.tag_price,
# 	t1.fact_price,
# 	t1.discount/t1.quantity AS discount,
# 	t4.promotion,
# 	-- t2.classfication_level AS class,
# 	0 AS label
# 	FROM tmp_kgs_all_data t1
# 	INNER JOIN tmp_kgs_test_data_all t2
# 	ON t1."id"=t2.id
# 	INNER JOIN ios_base_product t3
# 	ON t1."id"=t3.product_id
# 	LEFT JOIN
# 		(
# 		SELECT
# 		DISTINCT bar_code,promotion_date, 1 AS promotion
# 		FROM tmp_kgs_promotion
# 		) t4
# 	ON t3.bar_code=t4.bar_code AND CONCAT(EXTRACT(YEAR from t1."date"),'-',EXTRACT(MONTH from t1."date"))=t4.promotion_date
# 	WHERE t1."date">='2018-01-01'
# 	AND t1."id"=43791
# 	-- AND t2.classfication_level<6
# 	-- AND (t1."id"=44564 OR t1."id"=44655 OR t1."id"=46873 OR t1."id"=46876)
# 	ORDER BY "id","date"
# 	"""

sql="""
    SELECT
    t1.sku_id AS id,
    date(date) AS date,
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
    ON t1.sku_id=t2.sku_id
    WHERE t1.warehouse_id=1
    AND date>='2018-01-28'
    AND date<='2018-05-02'
	"""

input_data_df=pd.read_sql(sql, db)
# 将date列转成日期类型
input_data_df['date']=input_data_df['date'].map(lambda x: datetime.datetime.strptime(str(x),'%Y-%m-%d'))
print(input_data_df.head(2))
print(input_data_df.dtypes) #datetime64

config_sql='''
	SELECT
	date(work_day) AS date,
	holiday_type::VARCHAR AS holiday,
	month::VARCHAR AS season,
	is_weekend::VARCHAR AS weekend
	FROM 
	ios_base_work_calendar
	WHERE work_day>='2018-01-28'
	AND work_day<='2018-05-02'
	'''
config_data_df=pd.read_sql(config_sql, db)
# 将date列转成日期类型
config_data_df['date']=config_data_df['date'].map(lambda x: datetime.datetime.strptime(str(x),'%Y-%m-%d'))
# config_data_df['weekend_5']=config_data_df['weekend'].map(lambda x: x+5)

print(config_data_df.head())
print(config_data_df.dtypes) #datetime64


sql="""
    SELECT
    DISTINCT
    sku_id AS id,
    demand_class
    FROM ios_optimization_demand_classification
    WHERE warehouse_id=1
    """
rows = BaseModel.raw(sql)
demand_class_dict = dict()
for row in rows:
    id=str(row.id)
    demand_class=row.demand_class
    demand_class_dict[id]=demand_class
# print(demand_class_dict)


'''
SELECT
tb.* into tmp_ios_optimization_demand_classification_2
FROM 
	(SELECT
	ta.*,
	row_number() over(partition by demand_class ORDER BY random() DESC) AS rank
	FROM ios_optimization_demand_classification AS ta
	WHERE warehouse_id=1
	) AS tb
WHERE rank<=2
ORDER BY demand_class;
'''

# df_tmp=input_data_df[input_data_df['id']==11804]
# print(df_tmp.head())