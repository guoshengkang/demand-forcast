from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.warehouse import Warehouse
import datetime

class MoreLinesRate(BaseModel):
    class Meta:
        db_table = 'ios_sale_more_lines_rate'

    record_id = AutoField()
    store = ForeignKeyField(Store, null=True)
    warehouse = ForeignKeyField(Warehouse, null=True)
    book_date = DateTimeField(null=True)
    order_count = IntegerField(null=True)
    more_lines_order_count = IntegerField(null=True)
    more_lines_rate = DecimalField(max_digits=24, decimal_places=10)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
