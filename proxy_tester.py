#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool

import redis_proxy_pool


import requests
from queue import Queue
requests.packages.urllib3.disable_warnings()


'''
代理检测者
'''


class ProxyTester(object):
    def __init__(self):
        self.queue = Queue()
        self.running = False

        self.proxyPool = redis_proxy_pool.RedisProxyPool()

        self.pool = Pool(20)
        pass

    def _test_proxy(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
            }
            proxy = self.queue.get()
            proxy_obj = requests.utils.urlparse(proxy)

            if proxy_obj.scheme.upper() == 'HTTP':
                # test_url = 'https://www.qichacha.com/firm_3d0c5112a30ee9177e850c809c18bef4.html'
                # test_url = 'https://www.baidu.com/'
                test_url = 'https://www.sogou.com/reventondc/inner/vrapi?number=13700794549&type=json&callback=show&isSogoDomain=0'
                test_proxies = {
                    "http": proxy_obj.netloc
                }
            elif proxy_obj.scheme.upper() == 'HTTPS':
                # test_url = 'https://www.qichacha.com/firm_3d0c5112a30ee9177e850c809c18bef4.html'
                # test_url = 'https://www.baidu.com/'
                test_url = 'https://www.sogou.com/reventondc/inner/vrapi?number=13700794549&type=json&callback=show&isSogoDomain=0'
                test_proxies = {
                    "https": proxy_obj.netloc
                }
            else:
                return (False, proxy)
            response = requests.head(test_url,headers=headers,proxies=test_proxies,timeout=10,verify=False)
            if response.status_code == 200:
                return (True, proxy)
            else:
                return (False, proxy)
        except:
            return (False, proxy)

    def _test_proxy_finish(self, result):
        print(result)
        success, proxy = result
        if success:
            self.proxyPool.max(proxy)
        else:
            self.proxyPool.decrease(proxy)
        self.queue.task_done()
        self.pool.apply_async(self._test_proxy, callback=self._test_proxy_finish)

    def run(self):
        while True:
            proxies = self.proxyPool.all()
            if proxies is None or len(proxies) == 0:
                print("代理池为空")
                return

            self.running = True
            # 获取所有的代理
            for proxy in proxies:
                self.queue.put(proxy)
            for i in range(20):
                self.pool.apply_async(self._test_proxy, callback=self._test_proxy_finish)
            self.queue.join()
            time.sleep(60)


if __name__ == '__main__':
    tester = ProxyTester()
    tester.run()

