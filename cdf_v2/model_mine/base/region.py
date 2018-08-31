# -*- coding: utf-8 -*-

import datetime
from peewee import PrimaryKeyField, ForeignKeyField, CharField, IntegerField, DateTimeField, DecimalField

from base.base_module import BaseModel
from model.base.orgnization import Organization


class Region(BaseModel):
    class Meta:
        db_table = 'ios_base_region'

    region_id = PrimaryKeyField()
    organization = ForeignKeyField(Organization)
    name = CharField()
    status = IntegerField()
    parent_id = IntegerField()                       ##
    gen_time = DateTimeField(default=datetime.datetime.now)


class Region_Relation(BaseModel):
    class Meta:
        db_table = 'ios_base_region_relation'

    relation_id = PrimaryKeyField()
    region = ForeignKeyField(Region)
    type = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)


class Country(BaseModel):
    class Meta:
        db_table = 'ios_base_country'

    country_id = PrimaryKeyField()
    code = CharField()
    name = CharField()
    abbreviation_name = CharField()
    continent = IntegerField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)


class Province(BaseModel):
    class Meta:
        db_table = 'ios_base_province'

    province_id = PrimaryKeyField()
    country = ForeignKeyField(Country, related_name='province')
    name = CharField()
    abbreviation_name = CharField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)


class City(BaseModel):
    class Meta:
        db_table = 'ios_base_city'

    city_id = PrimaryKeyField()
    province = ForeignKeyField(Province, related_name='city')
    longtitude = DecimalField()
    latitude = DecimalField()
    name = CharField()
    abbreviation_name = CharField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)


class District(BaseModel):
    class Meta:
        db_table = 'ios_base_district'

    district_id = PrimaryKeyField()
    province = ForeignKeyField(Province)
    city = ForeignKeyField(City)
    longtitude = DecimalField()
    lantitude = DecimalField()
    name = CharField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)