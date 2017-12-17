#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from lxml import etree
import logging.config
from config.logging_config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('console')


class HtmlParser(object):

    def parser(self, html_cont):
        if html_cont is None:
            return
        html_soup = BeautifulSoup(html_cont, 'lxml')
        table_cont = html_soup.find_all(id='ip_list')
        table_soup = BeautifulSoup(str(table_cont), 'lxml')    # 转成bs对象才能进行搜索文档树
        ip_list_info = table_soup.table.contents               # .contents属性将Tag子节点以列表的方式输出

        proxy_list = []
        for index in range(len(ip_list_info)):
            if index % 2 == 1 and index != 1:                 # 索引为3,5,7...才是我们要的ip信息
                dom = etree.HTML(str(ip_list_info[index]))
                ip = dom.xpath('//td[2]')[0].text             # xpath中1为起始索引
                port = dom.xpath('//td[3]')[0].text
                protocol = dom.xpath('//td[6]')[0].text.lower()
                city = dom.xpath('//td[4]/a/text()')[0] if dom.xpath('//td[4]/a/text()') else '未知'
                date = dom.xpath('//td[10]')[0].text
                proxy_list.append({'ip': ip, 'port': port, 'protocol': protocol, 'city': city, 'update_date': date})
        return proxy_list
