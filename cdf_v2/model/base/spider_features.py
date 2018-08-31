import datetime
from base.base_module import BaseModel
from peewee import *

class SpiderFeatures(BaseModel):
    class Meta:
        db_table = 'ios_base_spider_features'

    spider_features_id = PrimaryKeyField()
    spider_features = CharField()
    status = CharField()
    gen_time = DateTimeField(default=datetime.datetime.now)

# SpiderFeatures.create_table()
# sf = SpiderFeatures()
# data = {'spider_features':'童装','status':'undo'}
# data = {'spider_features':'童装 羽绒服','status':'undo'}
# data = {'spider_features':'童装 裤子','status':'undo'}
# sf.insert(data).execute()