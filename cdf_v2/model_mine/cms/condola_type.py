#货架类型

from peewee import *
from base.base_module import BaseModel
import datetime

class Type(BaseModel):
    class Meta:
        db_table = 'cms_base_condola_type'


    type_id = AutoField()   #货架类型id
    type_code = CharField()  # 类型编码
    name = CharField()  #类型名称
    status = IntegerField(default=1)   #状态 0-无效 1-有效
    gen_time = DateTimeField(default=datetime.datetime.now)  # 创建时间