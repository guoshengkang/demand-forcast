#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-25 12:13:42
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

'''
创建视图的PG-SQL
'''
SELECT 
warehouse_id,
id,
book_date AS date,
-- 销量
max(CASE WHEN feature_name='quantity' and feature_type=0 THEN feature_value ELSE (NULL) END) AS quantity,
-- 标签价
max(CASE WHEN feature_name='tag_price' and feature_type=0 THEN feature_value ELSE (NULL) END) AS tag_price,
-- 销售价
max(CASE WHEN feature_name='fact_price' and feature_type=0 THEN feature_value ELSE (NULL) END) AS fact_price,
-- 毛利率
max(CASE WHEN feature_name='profit' and feature_type=0 THEN feature_value ELSE (NULL) END) AS profit,
-- 促销
max(CASE WHEN feature_name='promotion' and feature_type=1 THEN feature_value ELSE (0) END) AS promotion_1,
max(CASE WHEN feature_name='promotion' and feature_type=2 THEN feature_value ELSE (0) END) AS promotion_2,
max(CASE WHEN feature_name='promotion' and feature_type=3 THEN feature_value ELSE (0) END) AS promotion_3,
max(CASE WHEN feature_name='promotion' and feature_type=4 THEN feature_value ELSE (0) END) AS promotion_4,
max(CASE WHEN feature_name='promotion' and feature_type=5 THEN feature_value ELSE (0) END) AS promotion_5,
-- 新品
max(CASE WHEN feature_name='new_product' and feature_type=0 THEN feature_value ELSE (NULL) END) AS new_product,
-- 地域
max(CASE WHEN feature_name='city_tier' and feature_type=1 THEN feature_value ELSE (0) END) AS city_tier_1,
max(CASE WHEN feature_name='city_tier' and feature_type=2 THEN feature_value ELSE (0) END) AS city_tier_2,
max(CASE WHEN feature_name='city_tier' and feature_type=3 THEN feature_value ELSE (0) END) AS city_tier_3,
max(CASE WHEN feature_name='city_tier' and feature_type=4 THEN feature_value ELSE (0) END) AS city_tier_4,
max(CASE WHEN feature_name='city_tier' and feature_type=5 THEN feature_value ELSE (0) END) AS city_tier_5,
max(CASE WHEN feature_name='city_tier' and feature_type=6 THEN feature_value ELSE (0) END) AS city_tier_6,
-- 保质期
max(CASE WHEN feature_name='expiration' and feature_type=0 THEN feature_value ELSE (NULL) END) AS expiration,
-- 商圈
max(CASE WHEN feature_name='business_circle' and feature_type=1 THEN feature_value ELSE (0) END) AS business_circle_1,
max(CASE WHEN feature_name='business_circle' and feature_type=2 THEN feature_value ELSE (0) END) AS business_circle_2,
max(CASE WHEN feature_name='business_circle' and feature_type=3 THEN feature_value ELSE (0) END) AS business_circle_3,
max(CASE WHEN feature_name='business_circle' and feature_type=4 THEN feature_value ELSE (0) END) AS business_circle_4,
-- 店铺面积
max(CASE WHEN feature_name='shop_area' and feature_type=0 THEN feature_value ELSE (NULL) END) AS shop_area,
-- 新开业
max(CASE WHEN feature_name='new_opening' and feature_type=0 THEN feature_value ELSE (NULL) END) AS new_opening
FROM ios_product_feature_value
GROUP BY 	warehouse_id,	id,	book_date

############################################################################################

ios_optimization_product_feature_input

SELECT 
warehouse_id,
sku_id,
book_date AS date,
-- 销量
SUM(CASE WHEN feature_name='quantity' and feature_type=0 THEN feature_value ELSE (NULL)::double precision END) AS quantity,
-- 销售价
AVG(CASE WHEN feature_name='sale_price' and feature_type=0 THEN feature_value ELSE (NULL)::double precision END) AS sale_price,
-- 采购价
AVG(CASE WHEN feature_name='purchase_price' and feature_type=0 THEN feature_value ELSE (NULL)::double precision END) AS purchase_price,
-- 促销
SUM(CASE WHEN feature_name='promotion' and feature_type=1 THEN feature_value ELSE (0)::double precision END) AS promotion_1,
SUM(CASE WHEN feature_name='promotion' and feature_type=2 THEN feature_value ELSE (0)::double precision END) AS promotion_2,
SUM(CASE WHEN feature_name='promotion' and feature_type=3 THEN feature_value ELSE (0)::double precision END) AS promotion_3,
SUM(CASE WHEN feature_name='promotion' and feature_type=4 THEN feature_value ELSE (0)::double precision END) AS promotion_4,
SUM(CASE WHEN feature_name='promotion' and feature_type=5 THEN feature_value ELSE (0)::double precision END) AS promotion_5,
-- 产品状态
max(CASE WHEN feature_name='product_status' and feature_type=1 THEN feature_value ELSE (0)::double precision END) AS product_status_1,
max(CASE WHEN feature_name='product_status' and feature_type=2 THEN feature_value ELSE (0)::double precision END) AS product_status_2,
max(CASE WHEN feature_name='product_status' and feature_type=3 THEN feature_value ELSE (0)::double precision END) AS product_status_3,
max(CASE WHEN feature_name='product_status' and feature_type=4 THEN feature_value ELSE (0)::double precision END) AS product_status_4,
-- 库存状态
SUM(CASE WHEN feature_name='on_hand_quantity' and feature_type=0 THEN feature_value ELSE (NULL)::double precision END) AS on_hand_quantity
FROM ios_optimization_product_feature
GROUP BY 	warehouse_id,	sku_id,	book_date