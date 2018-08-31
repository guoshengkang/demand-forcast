from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.supplier import Supplier
from model.base.warehouse import Warehouse, WarehouseLocation
from model.base.product import Product,SKC, SKU
from model.base.replenishment_type import ReplenishmentType
from model.stock.stock_batch import StockBatch
import datetime


class StockReplenishment(BaseModel):
    class Meta:
        db_table = 'ios_optimization_stock_replenishment'

    record_id = AutoField()
    warehouse = ForeignKeyField(Warehouse, null=True) # ios_warehouse_id
    store = ForeignKeyField(Store, null=True)
    resource_warehouse = ForeignKeyField(Warehouse, null=True)  #
    resource_store = ForeignKeyField(Store, null=True)  # 来源门店id
    book_date = DateTimeField()                                         # < date 补货日期
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    rop = DecimalField(max_digits=24, decimal_places=10)                # 再订货点  < reorder_point
    ordering_cycle = IntegerField(null=True)                            # 订货周期
    ordering_quantity = DecimalField(max_digits=24, decimal_places=10)  # 订货批量
    type = ForeignKeyField(ReplenishmentType)                           # 补货策略  < order_policy
    quantity = DecimalField(max_digits=24, decimal_places=10)           # 补货数量  < num
    price = DecimalField(max_digits=24, decimal_places=10)              # 单价     < unit_price
    location = ForeignKeyField(WarehouseLocation)       #
    resource_location = ForeignKeyField(WarehouseLocation, null=True)
    status = DateTimeField(default=1)                   # 0: 无效, 1: 有效, 2: 已分销, 3: 已作废
    gen_time = DateTimeField(default=datetime.datetime.now)

    supplier = ForeignKeyField(Supplier)
    proposed_arrival_date = DateTimeField(null=True)
    batch = ForeignKeyField(StockBatch)
