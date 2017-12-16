#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
from config.spider_config import USER_AGENTS
import logging.config
from config.logging_config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('console')


class HtmlDownloader(object):

    def download(self, target_url):
        if target_url is None:
            return None
        # page = 1
        session = requests.Session()
        # target_url = 'http://www.xicidaili.com/nn/%d' % page
        user_agent = random.choice(USER_AGENTS)
        target_headers = {'Upgrade-Insecure-Requests': '1',
                          'User-Agent': user_agent,
                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                          'Referer': 'http://www.xicidaili.com/nn/',
                          'Accept-Encoding': 'gzip, deflate, sdch',
                          'Accept-Language': 'zh-CN,zh;q=0.8',
                          }
        target_response = session.get(target_url, headers=target_headers, timeout=5)
        if target_response.status_code == 200:
            target_response.encoding = 'utf-8'
            return target_response.text
        else:
            return None
