from peewee import *
from base.base_module import BaseModel
from .orgnization import Organization
import datetime


class Department(BaseModel):
    department_id = PrimaryKeyField()
    name = CharField(null=True)
    parent_id = IntegerField()
    is_sale_department = BooleanField(default=False)        # 销售部门标识
    is_purchase_department = BooleanField(default=False)    # 采购部门标识
    is_third_department = BooleanField(default=False)       # 第三方外部部门标识
    status = IntegerField(default=1)
    organization = ForeignKeyField(Organization)
    gen_time = DateTimeField(default=datetime.datetime.now)


