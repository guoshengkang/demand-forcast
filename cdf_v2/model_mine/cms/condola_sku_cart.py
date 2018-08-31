# 货架商品模型  显示已经摆放和未摆放

from peewee import *
from base.base_module import BaseModel
from model.base.product import Product,SKC,SKU
from model.cms.condola import Condola
from model.cms.condola_version import CondolaVersion
import datetime


class CondolaSkuCart(BaseModel):
    class Meta:
        db_table = 'cms_base_condola_sku_cart'

    record_id = AutoField()   # 记录id 自增主键
    condola = ForeignKeyField(Condola,null=True)  # 货架id
    version = ForeignKeyField(CondolaVersion,null=True)  # 版本id
    product = ForeignKeyField(Product,null=True)  # 商品id
    skc = ForeignKeyField(SKC, null=True)  # skcid
    sku = ForeignKeyField(SKU, null=True)  # skuid
    status = IntegerField(default=0,null=True)  # 状态  0-未摆放  1-已摆放
    gen_time = DateTimeField(default=datetime.datetime.now,null=True)  # 创建时间