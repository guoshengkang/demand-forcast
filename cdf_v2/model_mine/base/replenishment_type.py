from peewee import *
from base.base_module import BaseModel
import datetime


class ReplenishmentType(BaseModel):
    class Meta:
        db_table = 'ios_base_replenishment_type'

    replenishment_type_id = AutoField()
    name = CharField()                      # 补货策略名称
    status = IntegerField(default=1)        # 状态
    gen_time = DateTimeField(default=datetime.datetime.now)
