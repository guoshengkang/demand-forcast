# -*- coding: utf-8 -*-
import datetime
from peewee import AutoField, ForeignKeyField, IntegerField, DateTimeField, DecimalField
from base.base_module import BaseModel
from model.base.organization import Organization


class WarehouseType(BaseModel):
    '''
    工作日历
    '''
    class Meta:
        db_table = 'ios_base_work_calendar'

    record_id = AutoField()
    organization = ForeignKeyField(Organization, null=True)                             # 组织
    work_day = DateTimeField()                                                          # 日期
    year = IntegerField()                                                               # 年份
    season = IntegerField()                                                             # 季节
    month = IntegerField()                                                              # 月份
    week = IntegerField()                                                               # 周数
    week_day = IntegerField()                                                           # 星期几
    is_weekend = IntegerField(default=0)                                                # 是否周末 0-否 1-是
    is_holiday = IntegerField(default=0)                                                # 是否节假日 0-否 1-是
    holiday_type = IntegerField(default=0)                                              # 假期类型
    sale_influnce_type = IntegerField(default=0)                                        # 销量影响类型 0-无影响 1-当天销售会增加 2-当天销量会减少
    sale_influnce_weight = DecimalField(max_digits=24, decimal_places=10, null=True)    # 销售影响权重
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)