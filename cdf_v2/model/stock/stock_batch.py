from peewee import *
from base.base_module import BaseModel
from model.base.organization import Organization
from model.base.product import Product, SKU, SKC
from model.base.warehouse import Warehouse
import datetime

class StockBatch(BaseModel):
    class Meta:
        db_table = 'ios_stock_batch'

    batch_id = AutoField()  # 批次id

    organization = ForeignKeyField(Organization)
    batch_number = CharField(null=True)          # 批次号
    product_batch_number = CharField(null=True)  # 商品自身的批次号
    storage_date = DateTimeField(null=True)      # 入库日期

    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)

    shelflife_days = IntegerField()    # 保质期天数
    production_date = DateTimeField()  # 生产日期
    expiry_date = DateTimeField()    # 失效日期
    valid_days = IntegerField()      # 有效天数(每天计算)

    status = IntegerField(default=1)                                        # 状态
    gen_time = DateTimeField(default=datetime.datetime.now)                 # 创建日期