from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKU, SKC
from model.base.warehouse import WarehouseLocation
import datetime

class StockMove(BaseModel):
    class Meta:
        db_table = 'ios_stock_move'

    move_id = PrimaryKeyField()
    source_location = ForeignKeyField(WarehouseLocation)
    destination_location = (WarehouseLocation)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    quantity = DecimalField()
    move_time = DateTimeField()
    type = IntegerField()       # 0: 入库操作   # 1: 出库操作
    status = IntegerField(null=True)
    gen_time = DateTimeField(default=datetime.datetime.now)
