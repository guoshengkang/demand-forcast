from peewee import *
from base.base_module import BaseModel
from model.base.organization import Organization
from model.base.warehouse import Warehouse
from model.base.region import Region, Country, Province, City, District
import datetime

class Store(BaseModel):
    class Meta:
        db_table = 'ios_base_store'

    store_id = PrimaryKeyField()

    """ ----备份, 防止影响算法代码
    type = IntegerField()
    name = CharField()
    status = IntegerField()
    level = IntegerField()
    area = DecimalField()
    health_level = IntegerField()
    country = ForeignKeyField(Country)
    province = ForeignKeyField(Province)
    city = ForeignKeyField(City)
    district = ForeignKeyField(District)
    address = CharField()
    longtitude = DecimalField()
    latitude = DecimalField()
    price_type = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)
    warehouse = ForeignKeyField(Warehouse)
    region = ForeignKeyField(Region)"""

    type = IntegerField(default=2, null=True)  # 1. 加盟店   2. 直营店  3. 代理商  加盟店和直营店相对应的仓库都是门店仓，代理商相对应的就是代理仓，这个是刚加入的
    name = CharField()                  # 门店名称
    status = IntegerField(default=1)    # 状态:0-无效 1-有效
    level = IntegerField(null=True)     # 门店级别
    area = DecimalField(max_digits=24, decimal_places=10, null=True)   # 门店面积
    health_level = IntegerField(null=True)  # 库存健康状况
    country = ForeignKeyField(Country,null=True)
    province = ForeignKeyField(Province,null=True)
    city = ForeignKeyField(City,null=True)
    district = ForeignKeyField(District,null=True)
    address = CharField(null=True)
    longitude = DecimalField(max_digits=24, decimal_places=10, null=True)
    latitude = DecimalField(max_digits=24, decimal_places=10, null=True)
    price_type = IntegerField(null=True)    # 售价类型
    lead_time = IntegerField(default=1, null=True)     # 运输提前期
    bar_code = CharField(null=True)   # 门店识别码
    open_date = DateTimeField(null=True)  # 开业日期
    new_opening = IntegerField(null=True, default=2)  # 1:新开业   2:非新开业
    store_code = CharField(null=True)  # 门店编码
    district_type = CharField(null=True)  # 商圈类型  1-社区, 2-学校 3-办公 4-混合
    organization = ForeignKeyField(Organization, null=True)# 组织
    warehouse = ForeignKeyField(Warehouse, null=True)      # 仓库
    region = ForeignKeyField(Region, null=True)            # 区域
    gen_time = DateTimeField(default=datetime.datetime.now)
