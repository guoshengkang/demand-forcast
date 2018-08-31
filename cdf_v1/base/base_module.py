# -* - coding: UTF-8 -* -
from peewee import Model,PostgresqlDatabase
from base.config import cfg
from pymongo import MongoClient

#数据库实例对象  ----> 暂时还没有修改
db = PostgresqlDatabase(database=cfg.db_database,
                        host=cfg.db_addr,
                        port=cfg.db_port,
                        user=cfg.db_username,
                        password=cfg.db_password)

conn = MongoClient(cfg.mongodb_server, cfg.mongodb_port)
mongo_db = conn.sentiment  #连接sentiment数据库，没有则自动创建

class BaseModel(Model):
    class Meta:
        database = db