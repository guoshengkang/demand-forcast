# -*- coding: utf-8 -*-
import datetime
from peewee import PrimaryKeyField, CharField, DateTimeField, IntegerField, ForeignKeyField
from base.base_module import BaseModel

class FunctionRightType(BaseModel):
    class Meta:
        db_table = 'ios_base_fucntion_right_type'

    type_id = PrimaryKeyField()
    name = CharField()
    icon = CharField()
    index = IntegerField(default=0)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

class FunctionRight(BaseModel):
    class Meta:
        db_table = 'ios_base_function_right'

    function_right_id = PrimaryKeyField()                                   # 功能权限ID
    name = CharField()                                                      # 功能权限名称
    path = CharField()                                                      # 功能路径
    status = IntegerField(default=1)                                        # 状态 0-无效 1-有效
    description = CharField(null=True)                                      # 功能权限描述
    gen_time = DateTimeField(default=datetime.datetime.now)                 # 创建时间
    icon = CharField()                                                      # 图标
    index = IntegerField()                                                  # 获取的时候按照index升序排列.

    type = ForeignKeyField(FunctionRightType)


