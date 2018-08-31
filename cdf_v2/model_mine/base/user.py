# -*- coding: utf-8 -*-
import datetime

from model.base.role import Role
from model.base.data_right import DataRight
from peewee import *
from base.base_module import BaseModel
from model.base.orgnization import Organization
from model.base.department import Department
import datetime



# 用户模型
class User(BaseModel):
    class Meta:
        db_table = 'ios_base_user'
        order_by = ("last_login_time",)

    user_id = PrimaryKeyField()                                             # 用户ID
    password = CharField()                                                  # 密码
    name = CharField()                                                      # 姓名
    phone = CharField(unique=True)                                          # 手机号码
    email = CharField(unique=True, null=True)                               # 电子邮箱
    login_count = IntegerField(default=0)                                   # 登录次数
    last_login_time = DateTimeField(default=datetime.datetime.now)          # 最后登录时间
    is_manager = BooleanField(default=False)
    status = IntegerField(default=1)
    organization = ForeignKeyField(Organization)                            # 所属公司, 自动创建organization_id属性
    department = ForeignKeyField(Department)
    gen_time = DateTimeField(default=datetime.datetime.now)                 # 生成时间

# 用户系统关系表
class ThridSystemUserRelation(BaseModel):
    class Meta:
        db_table = 'ios_base_thrid_system_user_relation'

    relation_id = PrimaryKeyField()
    user = ForeignKeyField(User)                                            # 该用户在本系统中的表
    third_system_id = IntegerField()                                              # 其他系统的id
    # system_name = CharField()                                               # 其他系统的名称
    third_system_user_id = IntegerField()                                         # 该用户在其他系统中的id
    gen_time = DateTimeField(default=datetime.datetime.now)


# 用户 --- 角色 关系表
class UserRoleRelation(BaseModel):
    class Meta:
        db_table = 'ios_base_user_role_relation'

    relation_id = PrimaryKeyField()                                         # 关系ID
    user = ForeignKeyField(User)                                            # 用户
    role = ForeignKeyField(Role)                                            # 用户所具有的角色
    gen_time = DateTimeField(default=datetime.datetime.now)


# 用户 --- 数据权限 关系表
class UserDataRightRelation(BaseModel):
    class Meta:
        db_table = 'ios_base_user_data_rights_relation'

    relation_id = PrimaryKeyField()                                         # 关系ID
    user = ForeignKeyField(User)                                            # 用户
    data_right = ForeignKeyField(DataRight)                                 # 用户所具有的数据权限
    gen_time = DateTimeField(default=datetime.datetime.now)


# 用户日志
class UserLog(BaseModel):
    class Meta:
        db_table = 'ios_base_user_log'

    log_id = PrimaryKeyField()
    user = ForeignKeyField(User)                                            # 用户
    op_type = IntegerField()
    content = CharField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)                 # 生成时间


# VIP
class Vip(BaseModel):
    class Meta:
        db_table = 'ios_base_vip'

    vip_id = PrimaryKeyField()
    organization = ForeignKeyField(Organization)
    code = CharField()
    vip_user_id = IntegerField()             ##
    vip_user_name = CharField()
    vip_user_sex = IntegerField()
    vip_user_birthday = DateTimeField()
    vip_user_age = IntegerField()
    status = IntegerField()
    type = IntegerField()
    level = IntegerField()
    level_name = CharField()
    gen_time = DateTimeField(default=datetime.datetime.now)


class UserMessage(BaseModel):
    class Meta:
        db_table = 'ios_base_user_message'

    message_id = PrimaryKeyField()
    user = ForeignKeyField(User)
    type = IntegerField(default=1)
    message = CharField()
    content = CharField()
    sms_message = CharField()
    status = IntegerField(default=1)
    gen_time = DateTimeField(default=datetime.datetime.now)






