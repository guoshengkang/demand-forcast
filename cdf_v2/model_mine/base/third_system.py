from peewee import *
from base.base_module import BaseModel
import datetime

class ThirdSystem(BaseModel):
    class Meta:
        db_table = 'ios_base_third_system'

    third_system_id = PrimaryKeyField()
    name = CharField(null=True)
    app_key = CharField(null=True)
    security_key = CharField(null=True)
    third_system_app_key = CharField(null=True)
    third_system_security_key = CharField(null=True)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
