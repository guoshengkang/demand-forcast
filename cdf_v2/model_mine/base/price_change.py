# 门店调价表

from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.product import Product,SKC,SKU
import datetime

class PriceChange(BaseModel):
    class Meta:
        db_table = 'ios_base_price_change'

    record_id = AutoField()   # 记录id 自增主键
    store = ForeignKeyField(Store,null=True)  # 门店id
    product = ForeignKeyField(Product,null=True)  # 商品id
    skc = ForeignKeyField(SKC, null=True)  # skcid
    sku = ForeignKeyField(SKU, null=True)  # skuid
    old_sale_price = DoubleField(null=True)  # 原价格
    new_sale_price  = DoubleField(null=True)  #新价格
    start_date = DateTimeField(null=True)  #开始时间
    end_date = DateTimeField(null=True)  #结束时间
    status = IntegerField(default=1,null=True)  # 状态 默认有效 0-无效 1- 有效
    gen_time = DateTimeField(default=datetime.datetime.now,null=True)  # 创建时间