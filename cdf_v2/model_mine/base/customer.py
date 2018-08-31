from peewee import *
from base.base_module import BaseModel
from model.base.orgnization import Organization
from model.base.store import Store
import datetime

class Customer(BaseModel):
    class Meta:
        db_table = 'ios_base_customer'

    customer_id = PrimaryKeyField()
    name = CharField()
    type = IntegerField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)

class Saler(BaseModel):
    class Meta:
        db_table = 'ios_base_saler'

    saler_id = PrimaryKeyField()
    name = CharField()
    sex = IntegerField()
    birthday = DateTimeField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    store = ForeignKeyField(Store)