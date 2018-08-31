from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.warehouse import Warehouse, WarehouseLocation
from model.base.product import Product,SKC, SKU
import datetime

class StockReplenishment(BaseModel):
    class Meta:
        db_table = 'ios_optimization_stock_replenishment'

    record_id = PrimaryKeyField()
    warehouse = ForeignKeyField(Warehouse) # ios_warehouse_id
    store = ForeignKeyField(Store)
    book_date = DateTimeField()        # < date 补货日期
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    rop = DecimalField()
    ordering_cycle = IntegerField()
    ordering_quantity = DecimalField()
    type = IntegerField()
    quantity = DecimalField()           # < num 补货数量
    price = DecimalField()
    location = ForeignKeyField(WarehouseLocation)      ##
    status = DateTimeField()
    gen_time = DateTimeField(default=datetime.datetime.now)
