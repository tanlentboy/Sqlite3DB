# -*- coding: utf-8 -*-
import sqlite3
import random
import threading
#修改之后的伪多线程sqlite3数据库操作类
class SqliteDB:
    def __init__(self, database="SqliteDB.db"):
        self.local = threading.local()
        self.database = database

    def get_conn(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.database)
        return self.local.conn

    def get_cursor(self):
        if hasattr(self.local, 'cursor'):
            self.local.cursor.close()
        self.local.cursor = self.get_conn().cursor()
        return self.local.cursor

    def execute(self, sql):
        cursor = self.get_cursor()
        cursor.execute(sql)
        rowcount = cursor.rowcount
        return rowcount

    def delete(self, **kwargs):
        table = kwargs['table']
        where = kwargs['where']
        whereStr = ""
        if where is not None:
            whereStr = where
        sql = f"delete from {table} where {whereStr};"
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
            self.get_conn().commit()
        except:
            self.get_conn().rollback()
        return cursor.rowcount

    def insert(self, **kwargs):
        table = kwargs['table']
        del kwargs['table']
        sql = 'insert into %s(' % table
        fields = ""
        values = ""
        for k, v in kwargs.items():
            fields += "%s," % k
            values += "'%s'," % v
        fields = fields.rstrip(',')
        values = values.rstrip(',')
        sql = sql + fields + ")values(" + values + ")"
        print(sql)
        res = []
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
            self.get_conn().commit()
            res = cursor.lastrowid
        except:
            self.get_conn().rollback()
        return res

    def update(self, **kwargs):
        table = kwargs['table']
        kwargs.pop('table')
        where = kwargs['where']
        kwargs.pop('where')
        sql = 'update %s set ' % table
        for k, v in kwargs.items():
            sql += "%s='%s'," % (k, v)
        sql = sql.rstrip(',')
        sql += ' where %s' % where
        print(sql)
        rowcount = 0
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
            self.get_conn().commit()
            rowcount = cursor.rowcount
        except:
            self.get_conn().rollback()
        return rowcount

    def getOne(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s limit 1' % (field, table, where, order)
        print(sql)
        data = []
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()[0]
        except:
            self.get_conn().rollback()
        return data

    def getAll(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s ' % (field, table, where, order)
        print(sql)
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
        except:
            self.get_conn().rollback()
        return list(data)

    def createtb(self, sql=None, table=None, drop=None):
        if table is None:
            print("table参数不能为空")
            return False
        if drop is not None:
            self.droptb(table)
        cursor = self.get_cursor()
        cursor.execute(f"SELECT COUNT(*) FROM sqlite_master where type='table' and name='{table}'")
        values = cursor.fetchall()
        existtb = values[0][0]
        if existtb == 0:
            cursor.execute(sql)
        return cursor.rowcount

    def droptb(self, table=None):
        if table is None:
            print("表格不能为空")
            return False
        cursor = self.get_cursor()
        cursor.execute(f"drop table if exists {table};")
        return cursor.rowcount

    def close(self):
        if hasattr(self.local, 'conn'):
            self.local.conn.close()
            del self.local.conn
        if hasattr(self.local, 'cursor'):
            del self.local.cursor

    def __del__(self):
        self.close()
