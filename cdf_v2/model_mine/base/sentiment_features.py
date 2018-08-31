import datetime
from base.base_module import BaseModel
from peewee import *

class SentimentFeatures(BaseModel):
    class Meta:
        db_table = 'ios_base_sentiment_features'

    skc_id = IntegerField()
    name = CharField()
    sentiment_sale = IntegerField()
    sentiment_score = FloatField()
    sentiment_features = TextField()
    gen_time = DateField(default=datetime.datetime.now)

# SentimentFeatures.create_table()
sf = SentimentFeatures()
# data = {'skc_id':1,'name':'貂绒毛衣打底针织衫','sentiment_sale':100,'sentiment_score':0.95,'sentiment_features':''}
# sf.insert(data).execute()
# data = {'skc_id':2,'name':'针织长裤-脚口罗纹','sentiment_sale':100,'sentiment_score':0.95,'sentiment_features':''}
# sf.insert(data).execute()
# data = {'skc_id':3,'name':'棉风衣 黑色','sentiment_sale':100,'sentiment_score':0.95,'sentiment_features':''}
# sf.insert(data).execute()