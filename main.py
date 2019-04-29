import time
from multiprocessing import Process

from proxy_provider import ProxyProvider
from proxy_spider import ProxySpider
from proxy_tester import ProxyTester

spider = ProxySpider()

tester = ProxyTester()

proxy_spider = Process(target=spider.run)
proxy_spider.start()
proxy_test = Process(target=tester.run)
proxy_test.start()

proxyProvider = ProxyProvider()
proxyProvider.run()
proxy_spider.join()
proxy_test.join()
