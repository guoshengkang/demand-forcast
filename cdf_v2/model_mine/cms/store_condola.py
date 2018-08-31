# 门店和货架

from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.cms.condola import Condola
import datetime

class StoreCondola(BaseModel):
    class Meta:
        db_table = 'cms_base_store_condola'

    record_id = AutoField()   # 记录id  自增主键
    condola = ForeignKeyField(Condola)   #货架id
    store = ForeignKeyField(Store)    #门店id
    width = FloatField(null=True)    #长度
    height = FloatField(null=True)   # 高度
    angle = FloatField(null=True)    #角度
    direction = IntegerField(default=0)     #方向 0-横向 1-纵向
    location_x = FloatField(null=True)     #X坐标
    location_y = FloatField(null=True)     #Y坐标
    place_flag  = IntegerField(default=1,null=True)  # 陈列状态，0-未陈列 1-已陈列
    check_type = IntegerField(default=1)  #发布状态 0-草稿 1-发布
    status = IntegerField(default=1)    #状态 0-无效 1-有效
    gen_time = DateTimeField(default=datetime.datetime.now)  # 创建时间

