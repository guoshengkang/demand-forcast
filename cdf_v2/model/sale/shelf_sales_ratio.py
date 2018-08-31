from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.warehouse import Warehouse
from model.base.product import Product,SKC, SKU
import datetime

class ShelfSalesRatio(BaseModel):
    class Meta:
        db_table = 'ios_sale_shelf_sales_ratio'

    record_id = PrimaryKeyField()
    store = ForeignKeyField(Store)
    warehouse = ForeignKeyField(Warehouse)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    book_date = DateTimeField()
    sale_quantity = DecimalField()
    opening_inventory_quantity = DecimalField()
    ending_inventory_quantity = DecimalField()
    price = DecimalField()
    shelf_sales_ratio = DecimalField()
    gen_time = DateTimeField(default=datetime.datetime.now)
