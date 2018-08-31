from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.warehouse import Warehouse
from model.base.product import Product,SKC, SKU
import datetime

class StockParameter(BaseModel):
    class Meta:
        db_table = 'ios_optimization_stock_parameter'

    record_id = PrimaryKeyField()
    warehouse = ForeignKeyField(Warehouse)
    store = ForeignKeyField(Store)
    product = ForeignKeyField(Product)
    skc = ForeignKeyField(SKC)
    sku = ForeignKeyField(SKU)
    book_date = DateTimeField()
    rop = DecimalField()
    safety_stock = DecimalField()
    max_stock = DecimalField()
    min_stock = DecimalField()
    ordering_cycle = IntegerField()
    ordering_quantity = DecimalField()
    status = IntegerField()
    gen_time = DateTimeField(default=datetime.datetime.now)

# 仿真分析
class InventoryAnalysisModel(BaseModel):
    class Meta:
        db_table = 'ios_optimization_inventory_analysis'

    simulate_optimizate_id = PrimaryKeyField()  # 主键
    sku = ForeignKeyField(SKU, null=True)       # sku
    skc = ForeignKeyField(SKC, null=True)       # skc
    product = ForeignKeyField(Product, null=True)  # product
    warehouse = ForeignKeyField(Warehouse, null=True)  # warehouse

    cost_price = FloatField(null=True, default=0)  # 成本价
    sale_price = FloatField(null=True, default=0)  # 销售价
    sale_quantity = IntegerField(null=True, default=0)   # 销量
    classfication_level = CharField(null=True)  # 此sku对应的分类值
    classfication_value = CharField(null=True)  # 此sku原有的分类类型
    prediction_accuracy = DecimalField(max_digits=24, decimal_places=10, null=True, default=0.0)  # 预测精度
    valid_inventory_days = FloatField(null=True, default=0)  # 有效库存天数
    book_date = DateTimeField()

    n_y_max = FloatField(null=True, default=0)  # 仿真分析图标y轴最大值.
    o_y_max = FloatField(null=True, default=0)  # 仿真分析图标y轴最大值.
    y_max = FloatField(null=True, default=0)  # 仿真分析图标y轴最大值.

    n_ordering_quantity = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 订货批量(现状)
    ordering_quantity = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)    # 订货批量(优化后)

    cumulative_usage_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 累计使用价值
    o_cumulative_usage_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 累计使用价值

    o_eoq = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # eoq

    buyin_quantity = IntegerField(null=True, default=0)  # 采购量 现状
    o_buyin_quantity = IntegerField(null=True, default=0)  # 采购量  优化

    n_max_stock = FloatField(null=True, default=0.0)  # 平均最大库存
    o_max_stock = FloatField(null=True, default=0.0)  # 平均最大库存

    n_min_stock = FloatField(null=True, default=0.0)  # 平均最小库存 = 平均安全库存
    o_min_stock = FloatField(null=True, default=0.0)  # 平均最小库存 = 平均安全库存

    n_stock = FloatField(null=True, default=0.0)  # 平均库存
    o_stock = FloatField(null=True, default=0.0)  # 平均库存

    n_average_max_stock_days = FloatField(null=True, default=0.0)  # 平均最大库存天数
    o_average_max_stock_days = FloatField(null=True, default=0.0)  # 平均最大库存天数

    n_average_safety_stock_days = FloatField(null=True, default=0) # 平均安全库存天数
    o_average_safety_stock_days = FloatField(null=True, default=0) # 平均安全库存天数

    n_batch_size = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 订货批次
    o_batch_size = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 订货批次

    n_ordering_cycle = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 订货周期
    ordering_cycle = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 订货周期

    n_batch_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 批量价值
    o_batch_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 批量价值

    n_service_level = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状 服务水平(Service level)
    service_level = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 优化 服务水平(Service level)

    n_sum_holding_cost = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状 库存持有费用(Sum holding cost)
    o_sum_holding_cost = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 优化 库存持有费用(Sum holding cost)

    n_sum_ordering_cost = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状 订货费用(Sum ordering cost)
    o_sum_ordering_cost = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 优化 订货费用(Sum ordering cost)

    n_inventory_cost = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状 总库存成本(Inventory cost)
    o_inventory_cost = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 优化 总库存成本(Inventory cost)

    n_turn_days = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状 库存周转天数(Days Sales of Inventory)
    o_turn_days = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 优化 库存周转天数(Days Sales of Inventory)

    n_stock_capital = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状 库存资金占用量(Fund)
    o_stock_capital = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 优化 库存资金占用量(Fund)

    avg_gross_profit_margin = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状 毛利率(Gross Profit Margin)
    o_avg_gross_profit_margin = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 优化 毛利率(Gross Profit Margin)

    n_max_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状 平均最大库存价值(Average max stock value)
    o_max_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 优化 平均最大库存价值(Average max stock value)

    n_min_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 最小库存价值 / 安全库存价值
    o_min_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 最小库存价值 / 安全库存价值

    n_average_safety_stock = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 平均安全库存(Average safety stock)
    safety_stock = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)            # 平均安全库存(Average safety stock)

    n_safety_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 平均安全库存价值(Average safety stock value)
    o_safety_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 平均安全库存价值(Average safety stock value)

    n_stock_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 平均库存价值(Average on hand stock value)
    o_stock_value = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 平均库存价值(Average on hand stock value)

    n_result_image = CharField(null=True)  # 现状图片名称.
    o_result_image = CharField(null=True)  # 优化图片名称

    o_potential_savings_overage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 超储(优化)
    o_potential_savings_underage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0) # 短缺(优化)
    o_potential_quantity_overage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 超储数量(优化)
    o_potential_quantity_underage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0) # 短缺数量(优化)
    o_potential_savings = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 整体(优化)
    o_potential_quantity = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 整体数量(优化)

    n_potential_savings_overage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 超储(现状)
    n_potential_savings_underage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0) # 短缺(现状)
    n_potential_quantity_overage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 超储数量(现状)
    n_potential_quantity_underage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0) # 短缺数量(现状)
    n_potential_savings = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 整体(现状)
    n_potential_quantity = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 整体数量(现状)

    # compare_potential_savings_overage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状超储 - 优化超储(金额)
    # compare_potential_savings_underage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状短缺 - 优化短缺(金额)
    # compare_potential_quantity_overage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状超储 - 优化超储(数量)
    # compare_potential_quantity_underage = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状短缺 - 优化短缺(数量)
    # compare_potential_savings = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状整体 - 优化整体
    # compare_potential_quantity = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 现状整体 - 优化整体

    o_sales_revenue = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 由于缺货造成的销售损失(优化)
    n_sales_revenue = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 由于缺货造成的销售损失(现状)

    turn_days_saving = DecimalField(max_digits=24, decimal_places=10, null=True, default=0)  # 节约的周转天数

    gen_time = DateTimeField(default=datetime.datetime.now, null=True)