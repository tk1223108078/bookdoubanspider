# -*- coding: utf-8 -*-
import MySQLdb
import logging
import logging.config

# 配置文件使用好像有问题还是用代码配置把
# 采用配置文件配置
# logging.config.fileConfig('logging.conf')
# # 创建logger
# loggerInfo = logging.getLogger('infoLogger')

# 数据库操作类
class DbAcc:
    conn = None

    # 构造函数
    def __init__(self, host=None, user=None, passwd=None, dbname=None, port=None):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.port = port

    # 析构函数
    def __del__(self):
        if self.conn != None:
            # 关闭数据库连接
            self.conn.close()

    def dbconnect(self):
        result = True
        try:
            if self.dbname != None :
                self.conn = MySQLdb.connect(self.host, self.user, self.passwd, self.dbname, self.port)
            else:
                self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
        except Exception, e:
            logging.error(repr(e))
            result = False
        return  result

    # 选中数据库
    def dbselectdb(self, dbname=None):
        result = False
        if dbname != None:
            try:
                self.conn.select_db(dbname)
                result = True
            except Exception,e:
                logging.error(repr(e))
        return  result

    # 执行数据库操作
    def mysqlexecute(self, sql, *param):
        try:
            cursor = self.conn.cursor()
            response = cursor.fetchmany(cursor.execute(sql, param))
            self.conn.commit()
            result = True
        except Exception, e:
            logging.error(repr(e))
            result = False
        return result

