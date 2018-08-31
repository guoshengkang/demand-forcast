from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKC, SKU
from model.base.warehouse import WarehouseLocation
import datetime

class StockOnHand(BaseModel):
    class Meta:
        db_table = 'ios_stock_on_hand'

    on_hand_id = PrimaryKeyField()
    location = ForeignKeyField(WarehouseLocation)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    book_date = DateTimeField(null=True)
    init_quantity = DecimalField(max_digits=24, decimal_places=10)
    in_quantity = DecimalField(max_digits=24, decimal_places=10)
    out_quantity = DecimalField(max_digits=24, decimal_places=10)
    on_hand_quantity = DecimalField(max_digits=24, decimal_places=10)
    schedule_quantity = DecimalField(max_digits=24, decimal_places=10)
    on_passage_quantity = DecimalField(max_digits=24, decimal_places=10)
    init_amount = DecimalField(max_digits=24, decimal_places=10)
    in_amount = DecimalField(max_digits=24, decimal_places=10)
    out_amount = DecimalField(max_digits=24, decimal_places=10)
    sale_amount = DecimalField(max_digits=24, decimal_places=10)
    on_hand_amount = DecimalField(max_digits=24, decimal_places=10)
    schedule_amount = DecimalField(max_digits=24, decimal_places=10)
    on_passage_amount = DecimalField(max_digits=24, decimal_places=10)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
