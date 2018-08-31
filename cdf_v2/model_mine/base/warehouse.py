# -*- coding: utf-8 -*-

from peewee import *
from base.base_module import BaseModel
from model.base.algorithm import Algorithm
from model.base.region import Country, Province, City, District, Region
from model.base.organization import Organization
from model.base.product import ProductBrand
import datetime


class WarehouseType(BaseModel):
    """
    type_id==1: Store 门店
    type_id==2: RDC   地区仓
    type_id==3: DC    总仓
    type_id==4: PW    PlantWarehouse
    type_id==5: 电商仓
    """
    class Meta:
        db_table = 'ios_base_warehouse_type'

    type_id = PrimaryKeyField()
    name = CharField()                      # 类型名称
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

class Warehouse(BaseModel):
    class Meta:
        db_table = 'ios_base_warehouse'

    warehouse_id = PrimaryKeyField()                                                                        # 仓库ID
    organization = ForeignKeyField(Organization)                                                            # 所属组织
    brand = ForeignKeyField(ProductBrand)                                                                   # 所属品牌
    name = CharField()                                                                                      # 仓库名称
    type = ForeignKeyField(WarehouseType)                                                                   # 仓库类型
    barcode = CharField()                                                                                   # 仓库二维码
    longitude = DecimalField(max_digits=24, decimal_places=10, null=True, auto_round=True)                  # 经度
    latitude = DecimalField(max_digits=24, decimal_places=10, null=True, auto_round=True)                   # 纬度
    country = ForeignKeyField(Country)                                                                      # 所在国家
    province = ForeignKeyField(Province)                                                                    # 所在省份
    city = ForeignKeyField(City)                                                                            # 所在城市
    district= ForeignKeyField(District)                                                                     # 所在区县
    address = CharField()                                                                                   # 具体地址
    region = ForeignKeyField(Region)                                                                        # 所属地区
    classification_algorithm = ForeignKeyField(Algorithm)                                                   # 分类方法
    classification_number = IntegerField(default=6)                                                         # 分类数量
    classification_k_value = FloatField(default=50)                                                         # 分类K值
    classification_start_date = DateTimeField()                                                             # 分类计算开始日期
    classification_end_date = DateTimeField()                                                               # 分类计算结束日期
    current_classification_k_value = FloatField()                                                           # 当前k值
    average_ordering_cost = DecimalField(max_digits=24, decimal_places=10, default=0.00, auto_round=True)   # 平均订货成本
    percent_holding_cost = DecimalField(max_digits=24, decimal_places=10, default=0.15, auto_round=True)    # 持有成本比率
    service_level = DecimalField(max_digits=24, decimal_places=10, default=0.95, auto_round=True)           # 平均服务水平
    sevice_level_type = IntegerField(default=1)                                                             # 服务水平计算方式1-默认服务水平 2-分类服务水平 3-分类服务水平（如果为0则默认服务水平） 4-分类服务水平*权重系数 5-[分类服务水平（如果为0则默认服务水平）]*权重系数
    service_level_weight = FloatField(default=1.0)                                                          # 服务水平权重系数
    parent = ForeignKeyField('self', null=True, backref='children')                                         # 上级仓库
    lead_time = FloatField(default=1.0)                                                                     # 仓库订货提前期
    status = IntegerField(default=1)                                                                        # 当前状态 0-无效 1-有效
    gen_time = DateTimeField(default=datetime.datetime.now)                                                 # 创建时间

class WarehouseLocation(BaseModel):
    class Meta:
        db_table = 'ios_base_warehouse_location'

    location_id = PrimaryKeyField()
    warehouse = ForeignKeyField(Warehouse, backref='warehouse_location')
    location_type = IntegerField(default=1)      # 0: 在途  1: 库存,  默认计算查询都是使用1.  一个warehouse对应一个真实库存和一个在途库存
    name = CharField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)


