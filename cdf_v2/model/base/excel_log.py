from peewee import *
from base.base_module import BaseModel
from model.base.user import User
import datetime

class ExcelLog(BaseModel):
    class Meta:
        db_table = 'ios_base_excel_log'

    log_id = AutoField()
    user = ForeignKeyField(User)
    excel_name = CharField(null=True)            # 上传的excel原始文件名
    oss_excel_name = CharField()        # 上传至oss的excel文件对应的键值
    operation = IntegerField()          # 1: 上传  2：下载  3：取消
    msg = CharField(null=True)
    gen_time = DateTimeField(default=datetime.datetime.now)
    status = IntegerField(default=1)
