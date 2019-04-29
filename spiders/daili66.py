#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json

import requests


class Daili66ProxySpider(object):

    def get_url_list(self):
        return ['http://www.superfastip.com/api/ip?tid=005017f1619c415007d27577cc3e75b8&num=20&loc=中国&port=&an=12&type=1']


    def get_proxies(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        for url in self.get_url_list():
            response = requests.get(url, headers=headers)
            rows = json.loads(response.text)['ips']
            for idx in rows:

                ip = idx['ip']
                port = idx['port']
                type = idx['type'].lower()
                yield "{}://{}:{}".format(type, ip, port)

