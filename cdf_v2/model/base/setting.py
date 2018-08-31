from peewee import *
from base.base_module import BaseModel
from model.base.organization import Organization
import datetime

class Setting(BaseModel):
    class Meta:
        db_table = 'ios_base_setting'

    setting_id = PrimaryKeyField()
    organization = ForeignKeyField(Organization)

    setting_parameter = CharField(null=True)
    setting_value = CharField(null=True)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

    # 下列字段名, 对应setting_parameter字段, 值对应setting_value字段
    # year_days = IntegerField(default=365)               # 年工作日天数
    # week_days = IntegerField(default=7)                 # 星期工作日天数
    # forcast_cirlce_days = IntegerField(default=7)       # 预测期间天数
    # forcast_cirlce_number = IntegerField(default=5)     # 预测周期数
    # exchange_currency = CharField(default='RMB')        # 外币币种
    # exchange_rate = DecimalField(max_digits=24, decimal_places=10, default=1.000000)  # 外币汇率
    # start_day_of_week = IntegerField(default=1)         # 每周第一天 0:周日, 1:周一
    # sale_plan_type = IntegerField(default=1)            # 销售计划类型 0: 月计划, 1: 周期计划, 2: 天计划
    # caculate_time = TimeField(default=datetime.time(1,30,00))   # 运算开始时间 ----> 数据库中是timestamp类型, 但是默认值要求是01:30:00
    # classification_algorithm = ForeignKeyField(Algorithm)       # 分类算法
    # classification_number = IntegerField(default=6)      # 分类数量/库存分类数 < IosParameter.clasfy_num
    # ordering_cost = FloatField(default=0)                # (平均)订货成本
    # holding_cost = FloatField(default=0.15)              # (平均)持有成本
    # start_date_type = IntegerField(default=1)            # 默认运算开始日期, 0:当天, 1:昨天, 2:上周第一天, 3:上周最后一天, 4,本月第一天, 5:上月第一天, 6:本季第一天, 7:上季第一天, 8:本年第一天
    # sale_analysis_type = IntegerField(default=1)         #
    # aub_day = IntegerField(default=60)                   # 历史数据天数(分类用)
    # auf_day = IntegerField(default=30)                   # 预测日期天数(分类用)
    # classification_k_value = FloatField(default=50)      # 默认k值
    # default_service_level = FloatField(default=95.00)            # 服务水平
    # sale_plan_location_type = IntegerField(default=1)
    # default_classification_type

    # warehouse_typology_type = IntegerField(default=1)    # 1: DC-store, 2: DC1-store1 DC2-store2, 3: DC-RDC-store, 4: DC1-RDC1-store1 DC2-RDC2-store2, 5: PlantWarehouse(PW)-DC-RDC-store

