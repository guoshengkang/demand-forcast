from peewee import *
from base.base_module import BaseModel
from model.base.store import Store
from model.base.user import Vip
from model.base.product import Product, SKC, SKU
from model.base.organization import Organization
from model.base.customer import Customer
from model.base.customer import Saler
from model.base.warehouse import WarehouseLocation, Warehouse
import datetime

class SalePromotionPolicy(BaseModel):
    '''
    销售策略
    '''
    class Meta:
        db_table = 'ios_sale_promotion_policy'

    policy_id = AutoField()
    organization = ForeignKeyField(Organization)                                    # 公司
    start_time = DateTimeField()                                                    # 开始时间
    end_time = DateTimeField()                                                      # 结束时间
    type = IntegerField(default=1)                                                  # 类型： 1-满减(金额) 2-满减(数量) 3-满折(金额) 4-满折(数量) 5-加价送(金额) 6-加价送(数量) 7-满送(数量) 8-送积分
    is_order = IntegerField(default=1)                                              # 是否整单 0-否 1-是
    is_superposition = IntegerField(default=1)                                      # 是否可叠加 0-否 1-是
    mode = IntegerField(default=1)                                                  # 参与方式 0-白名单 1-黑名单
    discount_type = IntegerField(default=1)                                         # 折扣类型 0-百分比 1-金额
    discount_value = DecimalField(max_digits=24, decimal_places=10, null=True)      # 折扣额
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

class SalePromotionPolicyLine(BaseModel):
    '''
    销售策略明细
    '''
    class Meta:
        db_table = 'ios_sale_promotion_policy_line'

    record_id = AutoField()
    policy = ForeignKeyField(SalePromotionPolicy)                                   # 策略
    store = ForeignKeyField(Store, null=True)                                       # 门店/代理商
    warehouse = ForeignKeyField(Warehouse, null=True)                               # 仓库
    product = ForeignKeyField(Product, null=True)                                   # 商品
    sku = ForeignKeyField(SKU, null=True)                                           # SKC
    skc = ForeignKeyField(SKC, null=True)                                           # SKU
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

class SalePromotion(BaseModel):
    '''
    促销记录
    '''
    class Meta:
        db_table = 'ios_sale_promotion'

    promotion_id = AutoField()
    organization = ForeignKeyField(Organization)                                    # 公司
    policy = ForeignKeyField(SalePromotionPolicy)                                   # 策略
    store = ForeignKeyField(Store, null=True)                                       # 门店/代理商
    warehouse = ForeignKeyField(Warehouse, null=True)                               # 仓库
    product = ForeignKeyField(Product, null=True)                                   # 商品
    sku = ForeignKeyField(SKU, null=True)                                           # SKC
    skc = ForeignKeyField(SKC, null=True)                                           # SKU
    quantity = DecimalField(max_digits=24, decimal_places=10, null=True)            # 数量
    discount_amount  = DecimalField(max_digits=24, decimal_places=10, null=True)    # 数量
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

class Order(BaseModel):
    '''
    销售订单
    '''
    class Meta:
        db_table = 'ios_sale_order'

    order_id = AutoField()
    organization = ForeignKeyField(Organization)                                    # 组织
    customer = ForeignKeyField(Customer, null=True)                                 # 客户
    type = IntegerField(null=True)                                                  # 销售类型
    vip = ForeignKeyField(Vip, null=True)                                           # 会员
    sale_date = DateTimeField(null=True)                                            # 销售日期
    store = ForeignKeyField(Store, null=True)                                       # 门店/代理商
    location = ForeignKeyField(WarehouseLocation, null=True)                        # 仓库位置
    quantity = DecimalField(max_digits=24, decimal_places=10, null=True)            # 数量
    amount = DecimalField(max_digits=24, decimal_places=10, null=True)              # 销售金额
    discount = DecimalField(max_digits=24, decimal_places=10, null=True)            # 折扣金额
    saler = ForeignKeyField(Saler, null=True)                                       # 销售员
    order_code = CharField(null=True)                                               # 订单号
    promotion = ForeignKeyField(SalePromotion, null=True)                           # 促销记录
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)


class OrderLine(BaseModel):
    '''
    销售订单明细
    '''
    class Meta:
        db_table = 'ios_sale_order_line'

    line_id = AutoField()
    order = ForeignKeyField(Order, backref='orderlines')                            # 订单
    product = ForeignKeyField(Product, null=True)                                   # 商品
    sku = ForeignKeyField(SKU, null=True)                                           # SKC
    skc = ForeignKeyField(SKC, null=True)                                           # SKU
    quantity = DecimalField(max_digits=24, decimal_places=10, null=True)            # 数量
    price = DecimalField(max_digits=24, decimal_places=10, null=True)               # 单价
    sale_price = DecimalField(max_digits=24, decimal_places=10, null=True)          # 销售单价
    amount = DecimalField(max_digits=24, decimal_places=10, null=True)              # 金额
    discount = DecimalField(max_digits=24, decimal_places=10, null=True)            # 折扣
    promotion = ForeignKeyField(SalePromotion, null=True)                           # 促销记录
    purchase_price = DecimalField(max_digits=24, decimal_places=10, null=True)  # 采购
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)


class PreOrder(BaseModel):
    '''
    预销售订单明细（订货会）
    '''
    class Meta:
        db_table = 'ios_sale_pre_order'

    order_id = AutoField()
    book_date = DateTimeField()                                                     # 订单日期
    type = IntegerField()                                                           # 类型：0-订货会 1-翻单
    customer = ForeignKeyField(Customer, null=True)                                 # 客户
    store = ForeignKeyField(Store, null=True)                                       # 门店/代理商
    warehouse = ForeignKeyField(Warehouse, null=True)                               # 仓库
    product = ForeignKeyField(Product, null=True)                                   # 商品
    sku = ForeignKeyField(SKU, null=True)                                           # SKC
    skc = ForeignKeyField(SKC, null=True)                                           # SKU
    quantity = DecimalField(max_digits=24, decimal_places=10, null=True)            # 数量
    price = DecimalField(max_digits=24, decimal_places=10, null=True)               # 单价
    amount = DecimalField(max_digits=24, decimal_places=10, null=True)              # 金额
    comment = CharField(null=True)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)

class UpToNew(BaseModel):
    '''
    上新记录
    '''
    class Meta:
        db_table = 'ios_sale_up_to_new'

    record_id = AutoField()
    book_date = DateTimeField()                                                     # 上新日期
    store = ForeignKeyField(Store, null=True)                                       # 门店/代理商
    warehouse = ForeignKeyField(Warehouse, null=True)                               # 仓库
    product = ForeignKeyField(Product, null=True)                                   # 商品
    sku = ForeignKeyField(SKU, null=True)                                           # SKC
    skc = ForeignKeyField(SKC, null=True)                                           # SKU
    first_quanttiy = DecimalField(max_digits=24, decimal_places=10, null=True)      # 上新数量
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)