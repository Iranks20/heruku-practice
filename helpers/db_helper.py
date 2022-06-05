from flask import request
import pymysql
from config import DB_CONFIG as conf

DB = pymysql.connect(host=conf['host'], port=conf['port'], user=conf['username'], passwd=conf['password'],
                     db=conf['db'], autocommit=True, cursorclass=pymysql.cursors.DictCursor)
conn = DB.cursor()


class Database:
    def __init__(self):
        self.conn = conn

    @staticmethod
    def insert(table, **data):
        keys = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, keys)
        conn.execute(sql, values)
        last_id = conn.lastrowid
        return last_id

    @staticmethod
    def select(query):
        conn.execute(query)
        rows = conn.fetchall()
        return rows

    @staticmethod
    def delete(query):
        conn.execute(query)
        return True

    @staticmethod
    def selectData(query, params):
        conn.execute(query, params)
        rows = conn.fetchall()
        return rows

    @staticmethod
    def Update(table, where, **d):
        sql = 'UPDATE ' + table + ' SET {}'.format(', '.join('{}=%s'.format(k) for k in d))
        sql = sql + ' WHERE ' + where
        write_to_file(sql)
        values = tuple(d.values())
        conn.execute(sql, values)
        last_id = conn.lastrowid
        return last_id

    @staticmethod
    def SelectByList(table, column, list_of_ids):
        format_strings = ','.join(['%s'] * len(list_of_ids))
        conn.execute("SELECT * FROM " + table + " WHERE " + column + "  IN (%s)" % format_strings, tuple(list_of_ids))
        rows = conn.fetchall()
        return rows

    @staticmethod
    def SelectFeedList(table, column, list_of_ids, limit, order):
        format_strings = ','.join(['%s'] * len(list_of_ids))

        conn.execute("SELECT * FROM " + table + " WHERE " + column + "  IN (%s) AND feed_status = 'active' ORDER BY f_id DESC LIMIT 25" % format_strings, tuple(list_of_ids))
        rows = conn.fetchall()
        return rows

    @staticmethod
    def UpdateInt(table, where, **d):
        sql = 'UPDATE ' + table + ' SET {}'.format(', '.join('{}=%d'.format(k) for k in d))
        sql = sql + ' WHERE ' + where
        write_to_file(sql)
        values = tuple(d.values())
        conn.execute(sql, values)
        last_id = conn.lastrowid
        return last_id

    @staticmethod
    def UpdateData(table, where, data):
        sql = "UPDATE " + table + " SET % = %s WHERE " + where
        val = ("Valley", "Canyon")
        sql = "UPDATE " + table + " SET " + data + " WHERE " + where


    def write_to_file(data):
        f = open("output.txt", "w")
        f.write(data)
        f.close()
