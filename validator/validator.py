#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import time
import datetime
import threading
from config.spider_config import USER_AGENTS
import logging.config
from config.logging_config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('console')


class Validator(object):

    def __init__(self):
        self.user_agent = random.choice(USER_AGENTS)
        self.target_headers = {'Upgrade-Insecure-Requests': '1',
                               'User-Agent': self.user_agent,
                               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                               'Referer': 'http://www.xicidaili.com/nn/',
                               'Accept-Encoding': 'gzip, deflate, sdch',
                               'Accept-Language': 'zh-CN,zh;q=0.8',
                               }
        self.proxy_list = []
        self.https_proxy_list = []
        self.http_proxy_list = []

    def _check_https_proxy(self, https_proxy_list):
        valid_https_proxy_list = []
        for https_proxy in https_proxy_list:
            ip = https_proxy['ip']
            port = https_proxy['port']
            proxies = {
                "https": "http://" + ip + ":" + port    # "https": "http://10.10.1.10:1080"
            }
            try:
                requests.get('https://www.baidu.com/', headers=self.target_headers, proxies=proxies, timeout=3)
            except:
                # logger.warn('invalid https_proxy')
                pass
            else:
                valid_https_proxy_list.append(https_proxy)
        self.https_proxy_list = valid_https_proxy_list

    def _check_http_proxy(self, http_proxy_list):
        valid_http_proxy_list = []
        for http_proxy in http_proxy_list:
            ip = http_proxy['ip']
            port = http_proxy['port']
            proxies = {
                "http": "http://" + ip + ":" + port    # "http": "http://10.10.1.10:1080"
            }
            try:
                requests.get('http://www.guaishouxueyuan.net', headers=self.target_headers, proxies=proxies, timeout=3)
            except:
                # logger.warn('invalid http_proxy')
                pass
            else:
                valid_http_proxy_list.append(http_proxy)
        self.http_proxy_list = valid_http_proxy_list

    def check_proxy(self, proxy_list):
        self.https_proxy_list = [proxy for proxy in proxy_list if proxy['protocol'] == 'https']
        self.http_proxy_list = [proxy for proxy in proxy_list if proxy['protocol'] == 'http']

        threads = []
        t1 = threading.Thread(target=self._check_https_proxy, args=(self.https_proxy_list,))
        threads.append(t1)
        t2 = threading.Thread(target=self._check_http_proxy, args=(self.http_proxy_list,))
        threads.append(t2)

        starttime = datetime.datetime.now()
        logger.info('Start to validate...')
        for thread in threads:
            thread.setDaemon(True)
            thread.start()
        while True:
            alive = False
            for thread in threads:
                alive = alive or thread.isAlive()
            if not alive:
                break
            time.sleep(3)
        endtime = datetime.datetime.now()
        usedtime = (endtime - starttime).seconds
        logger.info('Validation completed,took %s seconds' % str(usedtime))
        self.proxy_list = self.https_proxy_list + self.http_proxy_list
        return self.proxy_list


if __name__ == '__main__':
    #validator = Validator()
    #validator.check_proxy([{'ip': '106.58.127.36', 'port': '80', 'protocol': 'https'}])
    starttime = datetime.datetime.now()
    endtime = datetime.datetime.now()
    usedtime = str((endtime - starttime).seconds)
