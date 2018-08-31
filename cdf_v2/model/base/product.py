from peewee import *
from base.base_module import BaseModel
from model.base.user import User
from model.base.organization import Organization, OrganizationTag
from model.base.images import Image
from model.base.static_data import StaticData
from model.base.supplier import Supplier
from model.base.factory import Factory
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


# class ProductCategory(BaseModel):
#     class Meta:
#         db_table = 'ios_base_product_category'
#
#     category_id = PrimaryKeyField()
#     name = CharField()
#     image = CharField()
#     parent_id = IntegerField()  ##
#     category_tree = CharField()
#     gen_time = DateTimeField(default=datetime.datetime.now)
#
#     brand_id = ForeignKeyField(ProductBrand)

class ProductCategory(BaseModel):
    class Meta:
        db_table = 'ios_base_product_category'

    category_id = AutoField()
    name = CharField()  # 分类名称
    image = ForeignKeyField(Image, null=True)  # 图片
    bar_code = CharField(null=True)  # 分类编码  是唯一的
    category_code = CharField(null=True)  # 分类编码
    parent_code = CharField(null=True)    # 上级分类编码
    index = IntegerField(default=0)  # 排序
    parent = ForeignKeyField('self', null=True, backref='children')  ##
    category_tree = CharField(null=True)  # 分类树链路 最顶级仓库: 1  下级仓库: 1_1, 1_2, 下下级仓库: 1_1_1, 1_1_2, 1_1_3
    gen_time = DateTimeField(default=datetime.datetime.now)
    status = IntegerField(default=1)
    brand = ForeignKeyField(ProductBrand)  # 品牌


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
    outlet_price = FloatField(null=True)  # 处理单价
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
    status = IntegerField(default=1)
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

    replenish_strategy_type = IntegerField(default=0, null=True)  # 0: 无策略, 1: 定量补货, 2: 定期补货, 3: 混合补货.

    safe_stock = DecimalField(max_digits=24, decimal_places=10, null=True)  # 安全库存
    ordering_cycle = IntegerField(null=True)  # 订货周期 todo 单位？
    ordering_quantity = DecimalField(max_digits=24, decimal_places=10, null=True)  # 订货批量
    max_stock = DecimalField(max_digits=24, decimal_places=10, null=True)  # 最大库存
    min_stock = DecimalField(max_digits=24, decimal_places=10, null=True)  # 最小库存
    rop = DecimalField(max_digits=24, decimal_places=10, null=True)  # 再订货点

    default_supplier = ForeignKeyField(Supplier, null=True)
    min_purchase_size = FloatField(null=True)
    min_distribution_size = FloatField(null=True)
    length = FloatField(null=True)
    width = FloatField(null=True)
    height = FloatField(null=True)
    purchase_width = FloatField(null=True)    # 采购商品宽度
    purchase_length = FloatField(null=True)   # 采购商品长度
    purchase_height = FloatField(null=True)   # 采购商品高度
    distribution_length = FloatField(null=True)  # 配送商品长度
    distribution_width = FloatField(null=True)   # 配送商品宽度
    distribution_height = FloatField(null=True)  # 配送商品高度
    gross_weight = FloatField(null=True)  # 毛重
    net_weight = FloatField(null=True)    # 净重
    vip_price = FloatField(null=True)     # 默认会员价
    brand_country = CharField(null=True)  # 品牌国家
    origin = CharField(null=True)         # 原产地
    shelflife_days = IntegerField(null=True)  # 保质期天数
    specification = CharField(null=True)      # 规格型号


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

# 商品原分类记录
class ProductClassification(BaseModel):
    class Meta:
        table_name = 'ios_base_product_classification'

    record_id = AutoField()  # ID
    book_date = DateTimeField()  # 记录日期
    product_id = ForeignKeyField(Product)  # 商品ID
    skc_id = ForeignKeyField(SKC)  # SKCID
    sku_id = ForeignKeyField(SKU)  # SKUID
    classification_algorithm = ForeignKeyField(StaticData)  # 分类算法
    classification_value = CharField()  # 分类值
    stage = IntegerField(null=True)  # 商品状态: X-新品, Z-正常, T-淘汰, Q-缺货.  # 文档中为"class", 作为关键字此处不能使用, 改为stage
    status = IntegerField(default=1)  # 状态 0-无效 1-有效
    gen_time = DateTimeField(default=datetime.datetime.now)  # 创建时间


class ProductionOrder(BaseModel):
    class Meta:
        table_name = 'ios_production_order'

    record_id = AutoField()
    organization_id = ForeignKeyField(Organization)
    order_number = CharField(null=True)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    department_id = IntegerField(null=True)
    factory = ForeignKeyField(Factory, null=True)
    quantity = DoubleField(null=True)
    book_date = DateTimeField(null=True)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now())


class ProductOrderLine(BaseModel):
    class Meta:
        table_name = 'ios_product_order_line'

    record_id = AutoField()
    order_id = ForeignKeyField(ProductionOrder)
    product_id = ForeignKeyField(Product, null=True)
    skc_id = ForeignKeyField(SKC, null=True)
    sku_id = ForeignKeyField(SKU, null=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    quantity = DoubleField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now())


class ProductPlan(BaseModel):
    class Meta:
        table_name = 'ios_product_plan'

    record_id = AutoField()
    type = IntegerField()             # 计划类型 0-SKU 1-SKC 2-商品 3-类别
    book_date = DateTimeField()       # 计划记录日期
    year = IntegerField(null=True)
    season = IntegerField(null=True)
    month = IntegerField(null=True)
    week = IntegerField(null=True)
    category_id = ForeignKeyField(ProductCategory, null=True)
    product_id = ForeignKeyField(Product, null=True)
    skc_id = ForeignKeyField(SKC, null=True)
    sku_id = ForeignKeyField(SKU, null=True)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    quantity = DoubleField()          # 计划数量
    category_number = IntegerField(null=True)  # 计划款数（服装行业), 针对type==3(类别)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now())


# 供应商商品对应关系
class SupplierProductRelation(BaseModel):
    class Meta:
        db_table = 'ios_base_supplier_product_relation'

    relation_id = AutoField()

    supplier = ForeignKeyField(Supplier)  # 供应商
    product = ForeignKeyField(Product)    # 商品
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    purchase_price = DecimalField(max_digits=24, decimal_places=10)  # 采购价
    lead_time = IntegerField(null=True)       # 生产提前提
    shelflife_days = IntegerField(null=True)  # 保质期天数
    start_date = DateTimeField(default=datetime.datetime.now)
    end_date = DateTimeField(default=datetime.datetime.now)

    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)  # 创建时间