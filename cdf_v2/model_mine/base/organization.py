# -*- coding: utf-8 -*-
import datetime
from peewee import PrimaryKeyField, CharField, DateTimeField, IntegerField, ForeignKeyField
from base.base_module import BaseModel

class Organization(BaseModel):
    class Meta:
        db_table = 'ios_base_organization'

    organization_id = PrimaryKeyField()                                     # 组织机构ID
    industry_id = IntegerField()                                            # 所属行业ID
    name = CharField(unique=True)                                           # 组织机构名称
    logo_icon = CharField(null=True)                                        # LOGO
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)                 # 创建时间


class IndustryStandardTag(BaseModel):
    class Meta:
        db_table = 'ios_base_industry_standard_tag'

    standard_tag_id = PrimaryKeyField()
    industry_id = IntegerField()
    type = IntegerField()
    code = CharField()
    value = CharField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)


class OrganizationTag(BaseModel):
    class Meta:
        db_table = 'ios_base_organization_tag'

    organization_tag_id = PrimaryKeyField()
    code = CharField()
    value = CharField()
    type = IntegerField()
    standard_tag_type = IntegerField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
    organization = ForeignKeyField(Organization)
    standard_tag = ForeignKeyField(IndustryStandardTag)


