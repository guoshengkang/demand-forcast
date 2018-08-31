from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKU, SKC
from model.base.store import Store
from model.base.warehouse import Warehouse
import datetime

class StockToSalesRate(BaseModel):
    class Meta:
        db_table = 'ios_stock_to_sales_rate'

    record_id = PrimaryKeyField()
    store = ForeignKeyField(Store)
    warehouse = ForeignKeyField(Warehouse)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    book_date = DateTimeField()
    sale_quantity = DecimalField()
    end_quantity = DecimalField()
    stock_to_sales_rate = DecimalField()
    gen_time = DateTimeField(default=datetime.datetime.now)
