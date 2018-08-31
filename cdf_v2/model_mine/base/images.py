from peewee import *
from base.base_module import BaseModel
import datetime

class Image(BaseModel):
    class Meta:
        db_table = 'ios_base_image'

    image_id = AutoField()

    protocol = CharField()
    oss_bucket = CharField()
    end_point = CharField()
    name = CharField()
    format = CharField()

    type = IntegerField(null=True)  # 未定.

    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
