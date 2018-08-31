from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKC, SKU
from model.base.store import Store
from model.base.warehouse import Warehouse
import datetime

class NewArrivalsRecord(BaseModel):
    class Meta:
        db_table = 'ios_stock_new_arrivals_record'

    record_id = PrimaryKeyField()                                                     #ID
    warehouse = ForeignKeyField(Warehouse)                                            #仓库
    store = ForeignKeyField(Store,null=True)                                          #门店
    product = ForeignKeyField(Product)                                                #商品
    skc = ForeignKeyField(SKC,null=True)                                              #SKC
    sku = ForeignKeyField(SKU,null=True)                                              #SKU
    book_date = DateTimeField()                                                       #上新日期
    quantity = DecimalField(max_digits=24, decimal_places=10,default=0.0,null=True)   #上新数量
    price = DecimalField(max_digits=24, decimal_places=10,default=0.0,null=True)      #上新单价
    amount = DecimalField(max_digits=24, decimal_places=10,default=0.0,null=True)     #上新金额
    status = IntegerField(default=1,null=True)                                        #状态 0-无效 1-有效
    gen_time = DateTimeField(default=datetime.datetime.now,null=True)                 #创建时间
