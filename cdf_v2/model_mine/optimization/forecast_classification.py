from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKU, SKC
from model.base.store import Store
from model.base.warehouse import Warehouse
import datetime

class ForecastClassification(BaseModel):
    class Meta:
        db_table = 'ios_optimization_forcast_classification'

    record_id = AutoField()

    warehouse = ForeignKeyField(Warehouse, null=True)
    product = ForeignKeyField(Product, null=True)

    skc = ForeignKeyField(SKC, null=True)
    sku = ForeignKeyField(SKU, null=True)

    adi_value = DecimalField(max_digits=24, decimal_places=10, null=True)
    cv2_value = DecimalField(max_digits=24, decimal_places=10, null=True)

    forecast_class = CharField()

    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
