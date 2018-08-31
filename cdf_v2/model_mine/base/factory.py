from peewee import *
from base.base_module import BaseModel
import datetime
from model.base.region import Country, Province, City, District
from model.base.organization import Organization

class Factory(BaseModel):
    class Meta:
        db_table = 'ios_base_factory'

    factory_id = AutoField()
    type = IntegerField()        # 类型 0-内部工厂 1-外协工厂
    name = CharField()
    factory_code = CharField(null=True)
    level = CharField(null=True)
    capacity = DecimalField(max_digits=24, decimal_places=10, null=True)  # 总产能
    country = ForeignKeyField(Country, null=True)
    province = ForeignKeyField(Province, null=True)
    city = ForeignKeyField(City, null=True)
    district = ForeignKeyField(District, null=True)
    address = CharField(null=True)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)
