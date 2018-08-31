from peewee import *
from base.base_module import BaseModel
from model.base.user import User
from model.base.orgnization import Organization, OrganizationTag
import datetime


class ProductBrand(BaseModel):
    class Meta:
        db_table = 'ios_base_product_brand'

    brand_id = PrimaryKeyField()
    name = CharField()
    image = CharField()
    description = CharField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)


class ProductCategory(BaseModel):
    class Meta:
        db_table = 'ios_base_product_category'

    category_id = PrimaryKeyField()
    name = CharField()
    image = CharField()
    parent_id = IntegerField()  ##
    category_tree = CharField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    brand_id = ForeignKeyField(ProductBrand)


class SizeGroup(BaseModel):
    class Meta:
        db_table = 'ios_base_size_group'

    size_group_id = PrimaryKeyField()
    name = CharField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)


class Size(BaseModel):
    class Meta:
        db_table = 'ios_base_size'

    size_id = PrimaryKeyField()
    name = CharField()
    status = IntegerField()
    index = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    size_group = ForeignKeyField(SizeGroup, related_name='size_group')


class Series(BaseModel):
    class Meta:
        db_table = 'ios_base_series'

    series_id = PrimaryKeyField()
    name = CharField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    brand = ForeignKeyField(ProductBrand)


class ColorGroup(BaseModel):
    class Meta:
        db_table = 'ios_base_color_group'

    color_group_id = PrimaryKeyField()
    name = CharField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)


class Color(BaseModel):
    class Meta:
        db_table = 'ios_base_color'

    color_id = PrimaryKeyField()
    name = CharField()
    status = IntegerField()
    index = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    color_group = ForeignKeyField(ColorGroup, related_name='color')


class Sex(BaseModel):
    class Meta:
        db_table = 'ios_base_sex'

    sex_id = PrimaryKeyField()
    name = CharField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)


class Unit(BaseModel):
    class Meta:
        db_table = 'ios_base_unit'

    unit_id = PrimaryKeyField()
    name = CharField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)

class UnitRelation(BaseModel):
    class Meta:
        db_table = 'ios_base_unit_relation'

    relation_unit_id = PrimaryKeyField()
    exchange_rate = DecimalField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    unit = ForeignKeyField(Unit, related_name='unit')
    

class Project(BaseModel):
    class Meta:
        db_table = 'ios_base_project'

    project_id = PrimaryKeyField()
    name = CharField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    status = IntegerField()
    pm_user_id = ForeignKeyField(User)
    description = CharField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)


class Model(BaseModel):
    class Meta:
        db_table = 'ios_base_model'

    model_id = PrimaryKeyField()
    name = CharField()
    year = IntegerField()
    season = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)


class Product(BaseModel):
    class Meta:
        db_table = 'ios_base_product'

    product_id = PrimaryKeyField()
    bar_code = CharField()
    standard_code = CharField()
    name = CharField()
    image = CharField()
    stock_unit_id = IntegerField()
    logistics_unit_id = IntegerField()
    year = IntegerField()
    season = IntegerField()
    designer_user_id = IntegerField(null=True)        ##
    designer_user = CharField(null=True)
    fabric1 = CharField()
    fabric2 = CharField()
    fabric3 = CharField()
    fabric4 = CharField()
    fabric5 = CharField()
    inner_fabric = CharField()
    fill_fabric = CharField()
    cost_price = FloatField()
    tag_price1 = FloatField()
    tag_price2 = FloatField()
    tag_price3 = FloatField()
    tag_price4 = FloatField()
    tag_price5 = FloatField()
    tag_price6 = FloatField()
    tag_price7 = FloatField()
    tag_price8 = FloatField()
    tag_price9 = FloatField()
    tag_price10 = FloatField()
    tag_price11 = FloatField()
    tag_price12 = FloatField()
    purchase_price = FloatField()
    retail_price = FloatField()
    tax_rate = FloatField()
    replenish_price = FloatField()
    distribution_price = FloatField()
    define1 = CharField()
    define2 = CharField()
    define3 = CharField()
    define4 = CharField()
    define5 = CharField()
    define6 = CharField()
    define7 = CharField()
    define8 = CharField()
    sale_days = IntegerField()
    sart_sale_date = DateTimeField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)
    project = ForeignKeyField(Project)
    sex = ForeignKeyField(Sex)
    unit = ForeignKeyField(Unit)
    brand = ForeignKeyField(ProductBrand)
    category = ForeignKeyField(ProductCategory)
    series = ForeignKeyField(Series)
    color_group = ForeignKeyField(ColorGroup)
    size_group = ForeignKeyField(SizeGroup)


class ProductTag(BaseModel):
    class Meta:
        db_table = 'ios_base_product_tag'

    product_tag_id = PrimaryKeyField()
    value = CharField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)
    organization_tag = ForeignKeyField(OrganizationTag)


class SKC(BaseModel):
    class Meta:
        db_table = 'ios_base_skc'

    skc_id = PrimaryKeyField()
    gen_time = DateTimeField(default=datetime.datetime.now)
    bar_code = CharField()  # 编码 / name

    organization = ForeignKeyField(Organization)
    brand = ForeignKeyField(ProductBrand)
    category = ForeignKeyField(ProductCategory)
    product = ForeignKeyField(Product)
    color = ForeignKeyField(Color)


class SKU(BaseModel):
    class Meta:
        db_table = 'ios_base_sku'

    sku_id = PrimaryKeyField()
    bar_code = CharField()  # 编码 / name
    gen_time = DateTimeField(default=datetime.datetime.now)

    organization = ForeignKeyField(Organization)
    brand = ForeignKeyField(ProductBrand)
    category = ForeignKeyField(ProductCategory)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    size = ForeignKeyField(Size)
    color = ForeignKeyField(Color)