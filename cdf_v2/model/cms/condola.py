# 货架模型类

from peewee import *
from base.base_module import BaseModel
from model.cms.condola_type import Type
from model.base.store import Store
from model.base.product import ProductCategory
import datetime


class Condola(BaseModel):
    class Meta:
        db_table = 'cms_base_condola'

    condola_id = AutoField()    # 货架id
    type_id = ForeignKeyField(Type,null=True)   #类型id
    condola_code = CharField(null=True)   # 货架编码
    name = CharField()      # 货架名称
    store = ForeignKeyField(Store,null=True)   # 门店id
    position = CharField(null=True)   # 货架位置
    width = FloatField(null=True)   # 货架宽度
    height = FloatField(null=True)   # 货架高度
    floor_height = CharField(null=True)  # 货架层高
    floor_weight = CharField(null=True)  #货架层深
    floor_position = CharField(null=True)  # 每层位置
    location_number = IntegerField(null=True)  # 货位个数
    floor_number = IntegerField(null=True)   #货架层数
    floor_type = CharField(null=True)    # 层板类型
    hole_distince = FloatField(null=True)  # 孔距
    hole_number = IntegerField(null=True)   # 孔数
    division_thickness = FloatField(null=True)  #隔板厚度
    align_type = IntegerField(null=True)   #对齐方式 0-左对齐 1-中对齐 2-右对齐
    level = CharField(null=True)   # 优先级
    abbreviation_name = CharField(null=True)   # 简称
    check_type = IntegerField(default=0,null=True)   #发布状态 0-草稿 1-发布
    status = IntegerField(default=0,null=True)     #状态 0-停用 1-启用
    category = ForeignKeyField(ProductCategory,null=True)  #存放的商品分类id
    gen_time = DateTimeField(default=datetime.datetime.now,null=True)   # 创建时间


