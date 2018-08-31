from peewee import *
from base.base_module import BaseModel
from model.base.organization import Organization
from model.base.store import Store
from model.base.warehouse import Region, Warehouse
import datetime

class DistributionPlan(BaseModel):
    class Meta:
        db_table = 'ios_optimization_distribution_plan'

    record_id = AutoField()
    plan_type = IntegerField(default=1)                         # 分销计划类型 0:首单, 1:翻单 2:补货
    distribution_type = IntegerField(default=1)                 # 分销计划类型 0:地区, 1:门店
    region = ForeignKeyField(Region)                            # 地区
    store = ForeignKeyField(Store, null=True)                   # 门店
    quantity = DecimalField(max_digits=24, decimal_places=10)   # 数量
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)
    warehouse = ForeignKeyField(Warehouse, null=True)