from peewee import *
from base.base_module import BaseModel
from model.base.supplier import Supplier
from model.base.product import Product, SKC, SKU
from model.base.warehouse import Warehouse
import datetime


# 采购订单
class PurchaseOrder(BaseModel):
    class Meta:
        db_table = 'ios_purchase_order'

    order_id = AutoField()
    order_number = CharField()
    supplier = ForeignKeyField(Supplier)
    warehouse = ForeignKeyField(Warehouse)
    book_date = DateTimeField()
    arrival_date = DateTimeField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)


class PurchaseOrderLine(BaseModel):
    class Meta:
        db_table = 'ios_purchase_order_line'

    order_line_id = AutoField()
    order = ForeignKeyField(PurchaseOrder)
    arrival_date = DateTimeField()
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    quantity = FloatField()
    price = FloatField()
    amount = FloatField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
