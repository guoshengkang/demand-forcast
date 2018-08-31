# 货架版本模型

from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.cms.condola import Condola
from model.base.user import User
import datetime

class CondolaVersion(BaseModel):
    class Meta:
        db_table = 'cms_base_condola_version'

    version_id = AutoField()  # 版本id
    version_code = CharField(null=True)  #版本编码
    condola = ForeignKeyField(Condola)  # 货架id
    store = ForeignKeyField(Store)  # 门店id
    user = ForeignKeyField(User)    #发布者的id
    status = IntegerField(default=1)   #状态 0-无效 1-有效
    gen_time = DateTimeField(default=datetime.datetime.now)  # 创建时间