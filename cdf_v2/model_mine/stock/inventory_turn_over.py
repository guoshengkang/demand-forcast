from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.warehouse import Warehouse
from model.base.product import Product, SKC, SKU
import datetime

class InventoryTurnOver(BaseModel):
    class Meta:
        db_table = 'ios_stock_inventory_turn_over'

    record_id = AutoField()
    store = ForeignKeyField(Store, null=True)
    warehouse = ForeignKeyField(Warehouse, null=True)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    opening_quantity = DecimalField(max_digits=24, decimal_places=10)
    ending_quantity = DecimalField(max_digits=24, decimal_places=10)
    sale_quantity = DecimalField(max_digits=24, decimal_places=10)
    inventory_carry_rate = DecimalField(max_digits=24, decimal_places=10)
    book_date = DateTimeField(null=True)
    status= IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
