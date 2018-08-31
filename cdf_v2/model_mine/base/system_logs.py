# -*- coding: utf-8 -*-
import datetime
from peewee import PrimaryKeyField, CharField, DateTimeField, ForeignKeyField, IntegerField
from base.base_module import BaseModel
from model.base.orgnization import Organization


class SystemLogs(BaseModel):
    class Meta:
        db_table = 'ios_base_system_logs'

    log_id = PrimaryKeyField()                                              # 日志ID
    organization = ForeignKeyField(Organization)
    type = IntegerField()                                                   # 日志类型 0-信息 1-警告 2-错误 3-DEBUG
    code = CharField()
    content = CharField()                                                   # 日志内容
    message = CharField()
    status = IntegerField()

    gen_time = DateTimeField(default=datetime.datetime.now)                 # 创建时间