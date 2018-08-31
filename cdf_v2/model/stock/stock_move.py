from peewee import *
from base.base_module import BaseModel
from model.base.product import Product, SKU, SKC
from model.base.warehouse import WarehouseLocation
from model.stock.stock_batch import StockBatch
import datetime

class StockMove(BaseModel):
    class Meta:
        db_table = 'ios_stock_move'

    move_id = AutoField()
    source_location = ForeignKeyField(WarehouseLocation, backref='stock_moves_source', null=True)
    destination_location = ForeignKeyField(WarehouseLocation, backref='stock_moves_destination', null=True)
    product = ForeignKeyField(Product, null=True)
    skc = ForeignKeyField(SKC, null=True)
    sku = ForeignKeyField(SKU, null=True)
    quantity = DecimalField(max_digits=24, decimal_places=10, null=True)  # 数量
    price = DecimalField(max_digits=24, decimal_places=10, null=True)     # 单价
    amount = DecimalField(max_digits=24, decimal_places=10, null=True)    # 金额 = 单价(price) * 数量(quantity)
    move_time = DateTimeField(null=True)
    type = IntegerField(default=1)   # 0: 入库操作   # 1: 出库操作

    order = IntegerField()  # 订单id(销售订单, 采购订单, 配货单, 生产订单, 有多种订单类型, 此字段不为外键字段)
    batch = ForeignKeyField(StockBatch)  # 订货批次id

    # mode字段值注释:
    # 入库   0
    #     采购入库单   1
    #     生产入库单   2
    #     期初入库单   3
    #     其他入库单   4
    #     销售退货入库单   5
    #     调拨入库单   6
    #     盘盈入库单   7
    #     分步式调入单 8
    #     批量调整入库单 9
    #     退料单      10
    #
    # 出库   1
    #     销售出库单   11
    #     调拨出库单   12
    #     其他出库单   13
    #     盘亏出库单   14
    #     分步式调出单  15
    #     批量调整出库单 16
    #     领料出库单   17
    mode = IntegerField(default=11)
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)
