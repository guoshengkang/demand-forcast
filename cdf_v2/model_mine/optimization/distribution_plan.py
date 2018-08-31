from peewee import *
from base.base_module import BaseModel
from model.base.orgnization import Organization
from model.base.store import Store
from model.base.warehouse import Region
import datetime

class DistributionPlan(BaseModel):
    class Meta:
        db_table = 'ios_optimization_distribution_plan'

    record_id = PrimaryKeyField()
    organization = ForeignKeyField(Organization)
    plan_type = IntegerField()
    distribution_type = IntegerField()  ##
    region = ForeignKeyField(Region)
    store = ForeignKeyField(Store)
    quantity = DecimalField()
    gen_time = DateTimeField(default=datetime.datetime.now)
