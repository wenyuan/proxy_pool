#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import logging.config
from config.logging_config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('console')

BASE_DIR = reduce(lambda x, y: os.path.dirname(x), range(2), os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data') if BASE_DIR else os.path.join(BASE_DIR, 'data')
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
DB_PATH = os.path.join(DATA_PATH, 'proxy_pool.db')


class SqliteHandle(object):

    def __init__(self):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute(' CREATE TABLE IF NOT EXISTS proxy_list (id INTEGER PRIMARY KEY AUTOINCREMENT, ip VARCHAR(20), '
                        'port VARCHAR(10), protocol VARCHAR(10), city VARCHAR(20), update_date VARCHAR(50) )')
            logger.info('Create or open table named proxy_list successfully')
        except Exception as e:
            logger.warn('Create table failed')
            logger.error(e)
        finally:
            cur.close()
            con.close()

    def insert_data(self, proxy_list):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        new_proxy_list = []
        for proxy in proxy_list:    # 去重处理
            ip = proxy['ip']
            port = proxy['port']
            protocol = proxy['protocol']
            condition = (ip, port, protocol)
            cur.execute(' SELECT * FROM proxy_list WHERE ip=? AND port=? AND protocol=?', condition)
            res = cur.fetchall()
            if not res:
                new_proxy_list.append(proxy)
        column_data = [
            (proxy['ip'], proxy['port'], proxy['protocol'], proxy['city'].decode('utf8'), proxy['update_date'].decode('utf8'))
            for proxy in new_proxy_list
        ]
        cur.executemany(' INSERT INTO proxy_list (ip,port,protocol,city,update_date) VALUES (?,?,?,?,?)', column_data)
        try:
            con.commit()
            row_count = cur.rowcount
            if row_count == -1:
                logger.info('Reduplicative data, none to insert')
            else:
                logger.info(('Insert %s rows successfully') % row_count)
        except Exception as e:
            con.rollback()
            logger.warn('Insert data failed')
            logger.error(e)
        finally:
            cur.close()
            con.close()

    def get_all_data(self):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute(' SELECT * FROM proxy_list')
        res = cur.fetchall()
        cur.close()
        con.close()
        result = []
        for line in res:
            result.append({'ip': line[1], 'port': line[2], 'protocol': line[3], 'city': line[4], 'update_date': line[5]})
        return result

    def get_data_by_condition(self, protocol, count):
        if protocol == 'https' or protocol == 'http':
            condition = (protocol, count)
        else:
            condition = ('*', count)
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute(' SELECT * FROM proxy_list WHERE protocol=? limit 0,?', condition)
        res = cur.fetchall()
        cur.close()
        con.close()
        result = []
        for line in res:
            result.append(
                {'ip': line[1], 'port': line[2], 'protocol': line[3], 'city': line[4], 'update_date': line[5]})
        return result

    def delete_invalid_data(self, proxy_list):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        condition = []
        for proxy in proxy_list:
            ip = proxy['ip']
            port = proxy['port']
            protocol = proxy['protocol']
            condition.append((ip, port, protocol))
        cur.executemany(' DELETE FROM proxy_list WHERE ip=? AND port=? AND protocol=?', condition)
        try:
            con.commit()
            row_count = cur.rowcount
            if row_count == 0:
                logger.info('No such data in databases')
            else:
                logger.info(('Delete %s rows successfully') % row_count)
        except Exception as e:
            con.rollback()
            logger.warn('Delete data failed')
            logger.error(e)
        finally:
            cur.close()
            con.close()

    def delete_table(self):
        con = sqlite3.connect(DB_PATH)
        con.execute('drop table proxy_list')
        logger.info('Delete table named proxy_list successfully')


if __name__ == '__main__':
    sqlite_handle = SqliteHandle()
    proxy_list = [{'ip': '127.0.0.1', 'port': 80, 'protocol': 'http', 'city': '中国', 'update_date': 'today'},
                  {'ip': '127.0.0.1', 'port': 90, 'protocol': 'https', 'city': '中国', 'update_date': 'today'},
                  {'ip': '127.0.0.1', 'port': 100, 'protocol': 'http', 'city': '中国', 'update_date': 'today'}]
    #sqlite_handle.insert_data(proxy_list)
    #sqlite_handle.get_all_data()
    #sqlite_handle.get_data_by_condition('httd',10)
    #sqlite_handle.delete_invalid_data(proxy_list)
    #sqlite_handle.delete_table()