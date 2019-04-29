import requests
from lxml import etree


class SuperFastIpSpider(object):
    def get_url_list(self):
        return ["http://www.superfastip.com/welcome/freeip/{}".format(i) for i in range(1, 10)]

    def get_proxies(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        for url in self.get_url_list():
            response = requests.get(url, headers=headers)
            edata = etree.HTML(response.text)
            rows = edata.xpath('//div[@class="row clearfix"][2]//tbody//tr')
            for idx in range(0, len(rows)):
                row = rows[idx]
                ip = row.xpath('./td[1]/text()')[0]
                port = row.xpath('./td[2]/text()')[0]
                type = row.xpath('./td[4]/text()')[0]
                yield "{}://{}:{}".format(type, ip, port)


# if __name__ == '__main__':
#     a = SuperFastIp()
#     s = a.get_proxies()
