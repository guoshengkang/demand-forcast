from peewee import *
from base.base_module import BaseModel
from model.base.warehouse import Warehouse
from model.base.product import Product, SKC, SKU
from model.base.algorithm import Algorithm
import datetime

class Classification(BaseModel):
    class Meta:
        db_table = 'ios_optimization_classificaition'

    classification_id = PrimaryKeyField()
    # organization = ForeignKeyField(Organization)
    warehouse = ForeignKeyField(Warehouse)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    cost_price= DecimalField()           # 成本价 < cost_price
    sale_price = DecimalField()
    opening_quantity = DecimalField()
    ending_quantity = DecimalField()     # 期末数量 < all_stock_qty
    sale_quantity = DecimalField()       # 出库数量
    buyin_quantity = DecimalField()      # 入库数量
    auv = DecimalField()                 # 订货周期
    ordering_cycle = IntegerField()         # 订货周期  < cycle
    ordering_quantity = DecimalField()       # 订货数量  < order_qty
    classfication_level = IntegerField()    # 分类      < line_type
    algorithm = ForeignKeyField(Algorithm)  # 使用的是哪一个算法
    status = IntegerField()
    number_of_batches = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)


class ClassificationK(BaseModel):
    class Meta:
        db_table = 'ios_optimization_classification_k'

    k_id = PrimaryKeyField()
    warehouse = ForeignKeyField(Warehouse)
    x_number_of_batches = DecimalField()
    y_inventory_value = DecimalField()
    value = DecimalField()
    gen_time = DateTimeField(default=datetime.datetime.now)

class ClassificationKCurveResultAll(BaseModel):
    class Meta:
        db_table = 'ios_optimization_classification_k_curve_result'

    result_id = PrimaryKeyField()
    sku_id = IntegerField()
    product_name = CharField()
    classfication_level = IntegerField()
    inventory_carry_rate = FloatField()
    inventory_carry_number = FloatField()
    current_period_inventory = FloatField()
    opening_quantity = IntegerField()
    ending_quantity = IntegerField()
    cost_price = FloatField()
    sale_quantity = IntegerField()
    buyin_quantity = IntegerField()
    auv = FloatField()
    color = CharField()
    size = IntegerField()
    sex = CharField()
    category = CharField()
    model = CharField()
    series = CharField()
    season = CharField()
    year = IntegerField()

class ClassificationKCurveResult(BaseModel):
    class Meta:
        db_table = 'ios_optimization_classification_k_curve_result'

    # result_id = PrimaryKeyField()
    sku_id = IntegerField()
    inventory_carry_rate = FloatField()
    current_period_inventory = FloatField()
    profit_rate = FloatField()
