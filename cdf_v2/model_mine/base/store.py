from peewee import *
from base.base_module import BaseModel
from model.base.orgnization import Organization
from model.base.warehouse import Warehouse
from model.base.region import Region, Country, Province, City, District
import datetime

class Store(BaseModel):
    class Meta:
        db_table = 'ios_base_store'

    store_id = PrimaryKeyField()

    type = IntegerField()
    name = CharField()
    status = IntegerField()
    level = IntegerField()
    area = DecimalField()
    health_level = IntegerField()
    country = ForeignKeyField(Country)
    province = ForeignKeyField(Province)
    city = ForeignKeyField(City)
    district = ForeignKeyField(District)
    address = CharField()
    longtitude = DecimalField()
    latitude = DecimalField()
    price_type = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)
    warehouse = ForeignKeyField(Warehouse)
    region = ForeignKeyField(Region)
