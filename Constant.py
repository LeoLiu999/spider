# -*- coding: utf-8 -*-

ORIGIN_URL = 'http://www.shuquge.com'  #抓取源地址
HEADER_HOST = 'www.shuquge.com' #header host
SITE_NAME = 'shuquge' #供工厂类使用 根据不同配置 实现不同的site类 抓取不同的站点

MAX_DEPTH = 5 #最大抓取深度
MAX_THREADS = 5 #最大抓取线程
THREAD_DELAY = 1 #线程延迟时间

REDIS_HOST = '127.0.0.1' #redis host
REDIS_PORT = 6379  #redis port

MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'db'
