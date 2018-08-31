from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKU, SKC
from model.base.warehouse import Warehouse
import datetime

class StockCount(BaseModel):
    class Meta:
        db_table = 'ios_stock_count'

    record_id = AutoField()
    warehouse = ForeignKeyField(Warehouse)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    type = IntegerField(default=1)                                          # 盘点类型 0-盘盈, 1-盘亏
    quantity = DecimalField(max_digits=24, decimal_places=10, null=True)    # 盘点数量
    book_date = DateTimeField(null=True)                                    # 盘点日期
    status = IntegerField(default=1)                                        # 状态
    gen_time = DateTimeField(default=datetime.datetime.now)                 # 创建日期