from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKC, SKU
from model.base.warehouse import WarehouseLocation
import datetime

class QuantityOnHand(BaseModel):
    class Meta:
        db_table = 'ios_stock_quantity_on_hand'

    hand_id = PrimaryKeyField()
    location = ForeignKeyField(WarehouseLocation)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    book_date = DateTimeField()
    quantity = DecimalField()
    gen_time = DateTimeField(default=datetime.datetime.now)
