# 货架s商品模型

from peewee import *
from base.base_module import BaseModel
from model.base.product import Product,SKC,SKU
from model.cms.condola import Condola
from model.cms.condola_version import CondolaVersion
import datetime


class CondolaSku(BaseModel):
    class Meta:
        db_table = 'cms_base_condola_sku'

    record_id = AutoField()   # 记录id 自增主键
    condola = ForeignKeyField(Condola)  # 货架id
    version = ForeignKeyField(CondolaVersion)  # 版本id
    floor = IntegerField(null=True)   # 层数
    floor_type = IntegerField(default=0)   #层板类型 0-平板 1-挂钩
    index = IntegerField(null=True)   # 序号
    product = ForeignKeyField(Product)  # 商品id
    skc = ForeignKeyField(SKC,null=True)   # skcid
    sku = ForeignKeyField(SKU, null=True)   # skuid
    align_left = FloatField(null=True)  # 左边距
    align_right = FloatField(null=True)  # 右边距
    angle = FloatField(null=True)   #角度
    direction = IntegerField(default=0)   # 方向 0-横向 1-纵向
    face = IntegerField(null=True)    # 排面数
    weight_number = IntegerField(null=True)  # 陈列量(每个排面）也叫深度
    status = IntegerField(default=1,null=True)  # 状态  0-无效 1-正常  2-禁售 3-禁配  4-淘汰  5-缺货
    remark = CharField(max_length=255,null=True)  # 备注
    gen_time = DateTimeField(default=datetime.datetime.now)  # 创建时间

'''货架id + 版本id + sku_id + 层数 + index   为联合唯一标识'''