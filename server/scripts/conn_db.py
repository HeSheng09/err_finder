import pymysql
import json
import sys


class ConnDb:
    def __init__(self):
        # super().__init__(self)
        with open(sys.path[0]+'/../config/db_connect.config', 'rt') as f:
            config = json.load(f)
        # 打开数据库连接
        self.conn = pymysql.connect(config['host'], config['user'], config['password'], config['db'], config['port'])

    def __del__(self):
        self.conn.close()
        # super().__del__(self)

    def select(self, obj, table, limitations):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self.conn.cursor()
        # 使用 execute()  方法执行 SQL 查询
        sql = "select " + obj + " from " + table + " where " + limitations
        if limitations == 'None':
            sql = sql.split('where')[0]
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def insert(self, table, cols, values):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO `" + table+"`("
            for col in cols:
                sql += '`'
                sql += col
                sql += '`,'
            sql = sql[0:len(sql) - 2]
            sql += "`) VALUE"
            if type(values) == str:
                sql += values
            else:
                for value in values:
                    sql += value
                    sql += ','
                sql = sql[0:len(sql) - 1]
            print(sql)
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return 'success'
        except:
            return 'fail'

    def insert_file(self, table, cols, values):
        try:
            cursor = self.conn.cursor()
            sql = "INSERT INTO `" + table+"`("
            for col in cols:
                sql += '`'
                sql += col
                sql += '`,'
            sql = sql[0:len(sql) - 2]
            sql += "`) VALUE("
            for value in values:
                if type(value) == bytes:
                    sql += '%s'
                else:
                    sql += value
                sql += ','
            sql = sql[0:len(sql) - 1]
            sql += ')'
            # print(sql)
            if type(values[1]) == bytes:
                cursor.execute(sql, pymysql.Binary(values[1]))
            else:
                cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return 'success'
        except:
            return 'fail'

    def delete(self, table, limitations):
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = self.conn.cursor()
            # 使用 execute()  方法执行 SQL 查询
            sql = "delete from " + table + " where " + limitations
            if limitations == 'None':
                sql = sql.split('where')[0]
            print(sql)
            cursor.execute(sql)
            return 'success'
        except:
            return 'fail'

    def update(self, table, cols, values, limitations):
        # UPDATE table_name SET field1=new-value1, field2=new-value2
        # [WHERE Clause]
        try:
            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = self.conn.cursor()
            # 使用 execute()  方法执行 SQL 查询
            sql = "update " + table + " set "
            for i in range(len(cols)):
                sql = sql + cols[i] + f"={values[i]}, "
            sql = sql[0:len(sql)-2]
            sql = sql + " where "+limitations
            if limitations == 'None':
                sql = sql.split('where')[0]
            print(sql)
            cursor.execute(sql)
            return 'success'
        except:
            return 'fail'