#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider.html_downloader import HtmlDownloader
from spider.html_parser import HtmlParser
from spider.url_manager import UrlManager
from validator.validator import Validator
from databases.sqlite_handle import SqliteHandle
import logging.config
from config.logging_config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('console')


class SpiderMan(object):

    def __init__(self):
        self.url_manager = UrlManager()
        self.html_downloader = HtmlDownloader()
        self.html_parser = HtmlParser()
        self.validator = Validator()
        self.sqlite_handle = SqliteHandle()

    def crawl(self, root_url):
        self.url_manager.add_new_url(root_url)
        while self.url_manager.has_new_url() and self.url_manager.old_url_size() < 100:
            try:
                new_url = self.url_manager.get_new_url()
                html_cont = self.html_downloader.download(new_url)
                proxy_list = self.html_parser.parser(html_cont)

                valid_proxy_list = self.validator.check_proxy(proxy_list)
                total_count = len(proxy_list)
                valid_count = len(valid_proxy_list)
                valid_rate = float(valid_count)/float(total_count)*100
                logger.info('total_count:%s, valid_count:%s, valid_rate:%.2f%%' % (str(total_count), str(valid_count), valid_rate))

                self.sqlite_handle.insert_data(valid_proxy_list)
                logger.info('Crawl→Download→Parse→Validate→Save: successfully')
            except Exception as e:
                logger.warn('Crawl→Download→Parse→Validate→Save: failed')
                logger.error(e)


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl('http://www.xicidaili.com/nn/1')
