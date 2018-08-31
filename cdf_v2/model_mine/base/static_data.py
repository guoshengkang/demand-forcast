from peewee import *
from base.base_module import BaseModel
import datetime

class StaticData(BaseModel):
    class Meta:
        db_table = 'ios_base_static_data'

    data_id = AutoField()
    name = CharField()
    english_name = CharField(null=True)
    type = IntegerField(default=1)  # 算法类型: 1:库存分类算法  2:销量预测算法  3:库存优化算法  4:补货算法
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)