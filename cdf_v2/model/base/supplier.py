from peewee import *
from base.base_module import BaseModel
from model.base.organization import Organization
from model.base.region import Region, Country, Province, City, District
import datetime

# 供应商
class Supplier(BaseModel):
    class Meta:
        db_table = 'ios_base_supplier'

    supplier_id = AutoField()
    supplier_code = CharField(null=True)  # 供应商编码
    supplier_name = CharField(null=True)  # 供应商名称

    organization = ForeignKeyField(Organization, null=True)  # 组织
    country = ForeignKeyField(Country,null=True)
    province = ForeignKeyField(Province,null=True)
    city = ForeignKeyField(City,null=True)
    district = ForeignKeyField(District,null=True)
    address = CharField(null=True)

    lead_time = IntegerField(default=1, null=True)  # 运输提前期
    otd_rate = DecimalField(max_digits=24, decimal_places=10)  # 订货及时率
    fill_rate = DecimalField(max_digits=24, decimal_places=10) # 到货满足率
    pass_rate = DecimalField(max_digits=24, decimal_places=10) # 质检合格率
    reject_rate = DecimalField(max_digits=24, decimal_places=10)  # 退货率
    average_arrival_days = FloatField()  # 商品平均有效天数

    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)  # 创建时间


