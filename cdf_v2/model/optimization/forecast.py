from peewee import *
from base.base_module import BaseModel
from model.base.user import User
from model.base.product import Product, SKC, SKU
from model.base.warehouse import Warehouse
from model.base.store import Store
from model.base.organization import Organization
import datetime


# 需求预测
class DemandForecast(BaseModel):
    class Meta:
        db_table = 'ios_optimization_demand_forecast'

    record_id = PrimaryKeyField()
    warehouse = ForeignKeyField(Warehouse)
    store = ForeignKeyField(Store)
    book_date = DateTimeField()         # 预测日期 < fore_date
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    start_date = DateTimeField()        # 开始日期 < s_date
    end_date = DateTimeField()          # 结束日期 < f_date
    cycle = IntegerField()
    forcast_days = IntegerField()
    quantity = DecimalField()            # 预测数量 < f_value
    status = IntegerField()
    calculate_record_id = IntegerField()
    data_type = IntegerField(default=1)  # 0: 真实数据  1: 拟合数据  2: 预测数据
    code = IntegerField(null=True)  # 对应码
    desc = CharField(null=True)     # 与code对应的描述
    model = CharField(null=True)
    gen_time = DateTimeField(default=datetime.datetime.now)


class FirstOrderForecast(BaseModel):
    class Meta:
        db_table = 'ios_optimization_first_order_forecast'

    record_id = PrimaryKeyField()
    organization = ForeignKeyField(Organization)
    year = IntegerField()
    season = IntegerField()
    month = IntegerField()
    week = IntegerField()
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    quantity = DecimalField()
    book_date = DateTimeField()
    gen_time = DateTimeField(default=datetime.datetime.now)


class ReorderForecast(BaseModel):
    class Meta:
        db_table = 'ios_optimization_recorder_forecast'

    record_id = PrimaryKeyField()
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    book_date = DateTimeField()
    reorder_cycle = IntegerField()
    reorder_date = DateTimeField()
    quantity = DecimalField()
    status = IntegerField()
    reject_reason = IntegerField()
    reject_reason_description = CharField()
    check_user_id = ForeignKeyField(User)
    check_time = DateTimeField()
    gen_time = DateTimeField(default=datetime.datetime.now)


class ProductFeatureType(BaseModel):
    class Meta:
        db_table = 'ios_optimization_product_feature_type'

    feature_id = AutoField()
    feature_type = IntegerField(null=True)          # 特征类型
    feature_name = CharField(Warehouse, null=True)  # 特征
    description = CharField(null=True)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)


class ProductFeature(BaseModel):
    class Meta:
        db_table = 'ios_optimization_product_feature'

    record_id = AutoField()

    store = ForeignKeyField(Store, null=True)  # 门店/代理商
    warehouse = ForeignKeyField(Warehouse, null=True)  # 仓库
    product = ForeignKeyField(Product, null=True)  # 商品
    sku = ForeignKeyField(SKU, null=True)  # SKC
    skc = ForeignKeyField(SKC, null=True)  # SKU
    book_date = DateTimeField(null=True)
    feature = ForeignKeyField(ProductFeatureType, null=True)

    feature_type = IntegerField(null=True)  # 特征类型
    feature_name = CharField(Warehouse, null=True)  # 特征
    feature_value = DecimalField(max_digits=24, decimal_places=10, null=True)  # 特征值

    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)


class DemandClassification(BaseModel):
    class Meta:
        db_table = 'ios_optimization_demand_classification'

    record_id = PrimaryKeyField()
    warehouse_id = ForeignKeyField(Warehouse)
    sku_id = ForeignKeyField(SKU)
    adi_value = DecimalField()
    cv2_value = DecimalField()
    demand_class = CharField()
    sale_days = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)