from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.warehouse import Warehouse
import datetime

class MoreLinesRate(BaseModel):
    class Meta:
        db_table = 'ios_sale_more_lines_rate'

    record_id = PrimaryKeyField()
    store = ForeignKeyField(Store)
    warehouse = ForeignKeyField(Warehouse)
    book_date = DateTimeField()
    order_count = IntegerField()
    more_lines_order_count = IntegerField()
    more_lines_rate = DecimalField()
    gen_time = DateTimeField(default=datetime.datetime.now)
