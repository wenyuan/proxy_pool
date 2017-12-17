#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sys

from databases.sqlite_handle import SqliteHandle

API_PORT = 12345
urls = (
    '/', 'Select',
    '/select', 'Select',
    '/delete', 'Delete'
)
sqlite_handle = SqliteHandle()


def start_api_server():
    sys.argv.append('0.0.0.0:%s' % API_PORT)
    app = web.application(urls, globals())
    app.run()


class Select(object):

    def GET(self):
        inputs = web.input()
        if not inputs:
            result = sqlite_handle.get_all_data()
        else:
            protocol = inputs.get('protocol', '*')    # http://127.0.0.1:12345/select?protocol=https&count=10
            count = inputs.get('count', 100)
            result = sqlite_handle.get_data_by_condition(protocol, count)
        return result


# todo...
class Delete(object):

    def GET(self):
        inputs = web.input()
        print(inputs.name, inputs.age)


if __name__ == '__main__':
    start_api_server()
