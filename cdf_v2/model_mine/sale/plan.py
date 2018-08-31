from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.warehouse import Region
from model.base.product import Product, ProductCategory, ProductBrand
from model.base.orgnization import Organization
from model.base.customer import Saler
import datetime

class Plan(BaseModel):
    class Meta:
        db_table = 'ios_sale_plan'

    plan_id = PrimaryKeyField()
    organization = ForeignKeyField(Organization)
    type = IntegerField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    year = IntegerField()
    season = IntegerField()
    month = IntegerField()
    week = IntegerField()
    region = ForeignKeyField(Region)
    store = ForeignKeyField(Store)
    saler = ForeignKeyField(Saler)
    brand = ForeignKeyField(ProductBrand)
    category = ForeignKeyField(ProductCategory)
    product = ForeignKeyField(Product)
    quantity = DecimalField()
    amount = DecimalField()
    parent_id = IntegerField()  ##
    gen_time = DateTimeField(default=datetime.datetime.now)
