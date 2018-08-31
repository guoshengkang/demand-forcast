from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKU, SKC
from model.base.store import Store
from model.base.warehouse import Warehouse
import datetime

class SellThroughRate(BaseModel):
    class Meta:
        db_table = 'ios_stock_sell_through_rate'

    record_id = PrimaryKeyField()
    store = ForeignKeyField(Store)
    warehouse = ForeignKeyField(Warehouse)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    sale_quantity = DecimalField()
    total_buyin_quantity = DecimalField()
    price = DecimalField()
    discount = DecimalField()
    sell_through_rate = DecimalField()
    book_date = DateTimeField()
    gen_time = DateTimeField(default=datetime.datetime.now)
