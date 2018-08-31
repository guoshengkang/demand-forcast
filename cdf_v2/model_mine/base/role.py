# -*- coding: utf-8 -*-
import datetime
from peewee import PrimaryKeyField, CharField, DateTimeField, ForeignKeyField, IntegerField
from base.base_module import BaseModel
from model.base.function_right import FunctionRight
from model.base.orgnization import Organization


class Role(BaseModel):
    class Meta:
        db_table = 'ios_base_role'

    role_id = PrimaryKeyField()                                                            # 角色ID
    name = CharField(unique=True)                                                          # 角色名称
    description = CharField(null=True)                                                     # 角色说明
    gen_time = DateTimeField(default=datetime.datetime.now)                                # 角色创建时间
    status = IntegerField(default=1)
    organization = ForeignKeyField(Organization)


class RoleFunctionRightRelation(BaseModel):
    class Meta:
        db_table = 'ios_base_role_function_right_relation'

    relation_id = PrimaryKeyField()
    role = ForeignKeyField(Role)
    function_right = ForeignKeyField(FunctionRight)
    gen_time = DateTimeField(default=datetime.datetime.now)
