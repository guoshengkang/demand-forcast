from peewee import *
from base.base_module import BaseModel
from model.stock.stock_batch import StockBatch
from model.base.store import Store
from model.base.product import Product, SKC, SKU
from model.base.warehouse import Warehouse
import datetime


# 采购订单
class DistributionOrder(BaseModel):
    class Meta:
        db_table = 'ios_distribution_order'

    order_id = AutoField()
    order_number = CharField()
    store = ForeignKeyField(Store)
    resource_warehouse = ForeignKeyField(Warehouse)
    book_date = DateTimeField()
    arrival_date = DateTimeField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)


class DistributionOrderLine(BaseModel):
    class Meta:
        db_table = 'ios_distribution_order_line'

    order_line_id = AutoField()
    order = ForeignKeyField(DistributionOrder)
    arrival_date = DateTimeField()
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    quantity = FloatField()
    price = FloatField()
    amount = FloatField()
    batch = ForeignKeyField(StockBatch)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
