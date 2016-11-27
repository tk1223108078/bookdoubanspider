# -*- coding: utf-8 -*-
import dbacc
import MySQLdb
import logging

DB_NAME = 'spider'
TABLE_NAME = 'book'

# 创建数据库连接
db = dbacc.DbAcc('127.0.0.1', 'root', 'kaige.19930730', None, 3306)
db.dbconnect()


def dbaccbook_initdb():
    result = False
    # 数据库不存在就创建
    sql = 'create database if not exists %s' % DB_NAME
    cursor = db.conn.cursor()
    cursor.execute(sql)
    # 表不存在就创建表
    # 这里设置No为自动增加
    sql = 'create table if not exists %s(No int auto_increment PRIMARY KEY NOT NULL, bookurl longtext not null, bookname longtext, bookauthor longtext,' \
          ' booktranslate longtext, bookpublic longtext, booktime longtext, bookprice longtext, bookscore longtext, booksubject longtext, booktag longtext)' % TABLE_NAME
    db.conn.select_db(DB_NAME)
    # UnicodeEncodeError: 'latin-1' codec can't encode characters in position 错误的解决方法，应该是字符设置的问题
    db.conn.set_character_set('utf8')
    cursor = db.conn.cursor()
    cursor.execute('set names utf8')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    cursor.execute(sql)
    return result


def dbaccbook_insertrecord(**record):
    cursor = db.conn.cursor()
    try:
        # 执行sql语句
        # 这样做的话MySQL模块会帮我们转义特殊字符，防止不必要的错误
        # 如果拼接字符串的时候这里需要加()将原组中的元素包裹起来，不然又会有参数个数不对的情况
        cursor.execute("INSERT INTO book(bookurl, bookname, bookauthor, booktranslate, \
          bookpublic, booktime, bookprice, bookscore, booksubject, booktag) \
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (record['bookurl'], record['bookname'], record['bookauthor'], record['booktranslate'],
                        record['bookpublic'], record['booktime'], record['bookprice'], record['bookscore'],
                        record['booksubject'], record['booktag']))
        # 提交到数据库执行
        db.conn.commit()
    except Exception, e:
        logging.error(repr(e))
        # 发生错误时回滚
        db.conn.rollback()
