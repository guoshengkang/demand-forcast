from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKU, SKC
from model.base.store import Store
from model.base.warehouse import Warehouse
import datetime

class CurrentPeriodInventory(BaseModel):
    class Meta:
        db_table = 'ios_stock_current_period_inventory'

    record_id = AutoField()

    store = ForeignKeyField(Store, null=True)           # 门店
    warehouse = ForeignKeyField(Warehouse, null=True)   # 仓库
    product = ForeignKeyField(Product)                  # 商品
    skc = ForeignKeyField(SKC)                          # SKC
    sku = ForeignKeyField(SKU)                          # SKU

    buyin_quantity = DecimalField(max_digits=24, decimal_places=10)             # 生产采购数量
    sale_quantity = DecimalField(max_digits=24, decimal_places=10)              # 销售数量
    current_period_inventory = DecimalField(max_digits=24, decimal_places=10)   # 产销比

    book_date = DateTimeField(null=True)                        # 记录日期
    status = IntegerField(default=1)                            # 状态
    gen_time = DateTimeField(default=datetime.datetime.now)
