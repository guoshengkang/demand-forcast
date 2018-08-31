from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.warehouse import Warehouse
from model.base.product import Product, SKC, SKU
import datetime

class InventoryCarryRate(BaseModel):
    class Meta:
        db_table = 'ios_stock_inventory_carry_date'

    record_id = PrimaryKeyField()
    store = ForeignKeyField(Store)
    warehouse = ForeignKeyField(Warehouse)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    opening_quantity = DecimalField()
    ending_quantity = DecimalField()
    sale_quantity = DecimalField()
    inventory_carry_rate = DecimalField()
    book_date = DateTimeField()
    gen_time = DateTimeField(default=datetime.datetime.now)
