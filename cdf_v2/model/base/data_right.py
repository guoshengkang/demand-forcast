# -*- coding: utf-8 -*-
import datetime
from peewee import PrimaryKeyField, CharField, DateTimeField, IntegerField, ForeignKeyField
from base.base_module import BaseModel
from model.base.organization import Organization


class DataRight(BaseModel):
    class Meta:
        db_table = 'ios_base_data_right'

    data_right_id = PrimaryKeyField()                                       # 数据权限ID
    name = CharField()                                                      # 数据权限名称
    type = IntegerField(null=True)
    data_code = CharField(null=True)                                             # 所属数据
    data_value = CharField(null=True)
    status = IntegerField(default=1)                                        # 状态 0-无效 1-有效
    description = CharField(null=True)                                      # 数据权限描述
    gen_time = DateTimeField(default=datetime.datetime.now)                 # 创建时间

    organization = ForeignKeyField(Organization)
