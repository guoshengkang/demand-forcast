from peewee import *
from base.base_module import BaseModel
import datetime

class Algorithm(BaseModel):
    class Meta:
        db_table = 'ios_base_algorithm'

    algorithm_id = PrimaryKeyField()
    name = CharField()
    type = IntegerField()  # 算法类型: 0:库存分类算法  1:销量预测算法  2:库存优化算法  3:补货算法
    gen_time = DateTimeField(default=datetime.datetime.now)
