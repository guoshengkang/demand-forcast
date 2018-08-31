# -* - coding: UTF-8 -* -

from configparser import ConfigParser
import os

class ServerConfig():

    #数据库默认配置信息
    db_addr,db_database,db_username,db_password,db_port = "172.12.78.217","ios2","postgres","Password123",5432
    #spark配置信息
    spark_master,spark_port,app_name='172.12.78.152',7077,'ios'
    #hadoop配置信息
    hadoop_namenode,hadoop_port,db_name='172.12.78.151',8088,'ios'
    #REDIS默认配置信息
    redis_addr,redis_port,redis_auth= "172.12.78.217","6379","Password123"
    #mongodb默认配置信息
    mongodb_server = "172.12.78.217"
    mongodb_port = 27017
    # 画图相关
    plot_font_path = '/usr/share/fonts/truetype/dejavu/PingFang.ttc'
    #服务器默认配置信息
    server_addr,server_port="0.0.0.0",5000
    #调度默认配置信息
    shutdown_server_wait = 300
    spider_job_hour, spider_job_minitue = 0, 1
    tag_job_hour,tag_job_minitue = 1,30
    classification_job_hour,classification_job_minitue = 2,30
    forcast_job_hour,forcast_job_minitue = 3,30
    reorder_job_hour,reorder_job_minitue = 4,30

    # 读取配置文件
    if os.path.exists("server.conf"):
        print ('read config from file')
        try:
            conf = ConfigParser()
            conf.read('server.conf')
            # 读取数据库配置
            db_addr = conf.get("postgresql", "server")
            db_port = conf.getint("postgresql", "port")
            db_database = conf.get("postgresql", "database")
            db_username = conf.get("postgresql", "username")
            db_password = conf.get("postgresql", "password")
            # 读取REDIS配置
            mongodb_server = conf.get("redis", "server")
            redis_port = conf.getint("redis", "port")
            redis_auth = conf.get("redis", "auth")
            # 读取MONGODB配置
            redis_addr = conf.get("mongodb", "server")
            mongodb_port = conf.getint("mongodb", "port")
            # 读取SPARK配置
            spark_master = conf.getint("spark", "master")
            spark_port = conf.getint("spark", "port")
            app_name = conf.getint("spark", "app_name")
            # 读取HADOOP配置
            hadoop_namenode = conf.getint("hadoop", "namenode")
            hadoop_port = conf.getint("hadoop", "port")
            db_name = conf.getint("hadoop", "db_name")
            # 画图相关
            plot_font_path = conf.getint("plot", "font_path")
            # 读取系统配置
            server_addr = conf.get("server", "addr")
            server_port = conf.getint("server", "port")
            # 读取调度配置
            spider_job_hour = conf.getint("job", "spider_job_hour")
            spider_job_minitue = conf.getint("job", "spider_job_minitue")
            tag_job_hour = conf.getint("job", "tag_job_hour")
            tag_job_minitue = conf.getint("job", "tag_job_minitue")
            classification_job_hour = conf.getint("job", "classification_job_hour")
            classification_job_minitue = conf.getint("job", "classification_job_minitue")
            forcast_job_hour = conf.getint("job", "forcast_job_hour")
            forcast_job_minitue = conf.getint("job", "forcast_job_minitue")
            reorder_job_hour = conf.getint("job", "reorder_job_hour")
            reorder_job_minitue = conf.getint("job", "reorder_job_minitue")
            shutdown_server_wait = conf.getint("job", "shutdown_server_wait")
        except KeyError as e:
            pass

cfg = ServerConfig()