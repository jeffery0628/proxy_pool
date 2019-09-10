from lxml import etree
from proxypool.utils import get_page

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):

    def __init__(self,cfg):
        self.cfg = cfg


    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_xicidaili(self):
        types = self.cfg.get('xici', 'types').lstrip('[').rstrip(']').split(',')
        page_num = int(self.cfg.get('xici', 'page_num'))
        url = self.cfg.get('xici', 'url')

        for type in types:
            for page in range(1,page_num):
                proxy_list_url = url.format(type,page)
                response_text = get_page(proxy_list_url)
                if response_text:
                    html = etree.HTML(response_text)
                    trs = html.xpath('//table[@id="ip_list"]//tr')[1:]
                    for tr in trs:
                        ip = tr.xpath('./td[2]/text()')[0]
                        port = tr.xpath('./td[3]/text()')[0]
                        scheme = tr.xpath('./td[6]/text()')[0].lower()
                        # 拼接代理
                        proxy = '%s://%s:%s' % (scheme, ip, port)
                        yield proxy,ip,port,scheme

    # 获取代理66
    def crawl_daili66(self, page_count=4):


        url = self.cfg.get('daili-66','url')
        page_num = int(self.cfg.get('daili-66','page_num'))
        for page in range(1,page_num):
            # 拼接要爬取的url
            proxy_list_url = url.format(page)
            # 该网页需要动态渲染，设置selenium=True,使用selenium 爬取
            browser = get_page(url=proxy_list_url,selenium=True)
            if browser:
                # 因为tr[0]是标题
                trs = browser.find_elements_by_xpath('//div[@align="center"]/table/tbody/tr')[1:]
                for tr in trs:
                    res = tr.text.split(' ')
                    ip = res[0]
                    port = res[1]
                    scheme = 'https'
                    # 拼接代理
                    proxy = '%s://%s:%s' % (scheme, ip, port)
                    yield proxy,ip,port,scheme



    def crawl_ip3366(self):
        types = self.cfg.get('ip-3366','types').lstrip('[').rstrip(']').split(',')
        page_num = int(self.cfg.get('ip-3366','page_num'))
        url = self.cfg.get('ip-3366','url')
        for type in types:
            for page in range(1, page_num):
                proxy_list_url = url.format(type,page)
                response_text = get_page(url=proxy_list_url)
                if response_text:
                    html = etree.HTML(response_text)
                    trs = html.xpath('//div[@id="list"]/table/tbody/tr')
                    for tr in trs:
                        ip = tr.xpath('./td[1]/text()')[0]
                        port = tr.xpath('./td[2]/text()')[0]
                        scheme = tr.xpath('./td[4]/text()')[0].lower()
                        # 拼接代理
                        proxy = '%s://%s:%s' % (scheme, ip, port)
                        yield proxy,ip,port,scheme


    def crawl_kuaidaili(self):
        types = self.cfg.get('kuaidaili','types').lstrip('[').rstrip(']').split(',')
        page_num = int(self.cfg.get('kuaidaili','page_num'))
        url = self.cfg.get('kuaidaili','url')

        for type in types:
            for page in range(1,page_num):
                proxy_list_url = url.format(type,page)
                response_text = get_page(url=proxy_list_url)
                if response_text:
                    html = etree.HTML(response_text)
                    trs = html.xpath('//table/tbody/tr')
                    for tr in trs:
                        ip = tr.xpath('./td[@data-title="IP"]/text()')[0]
                        port = tr.xpath('./td[@data-title="PORT"]/text()')[0]
                        scheme = tr.xpath('./td[4]/text()')[0].lower()
                        # 拼接代理
                        proxy = '%s://%s:%s' % (scheme, ip, port)
                        yield proxy,ip,port,scheme


    def crawl_iphai(self):
        url = self.cfg.get('iphai','url')

        response_text = get_page(url)
        if response_text:
            html = etree.HTML(response_text)
            trs = html.xpath('//table//tr')[1:]
            for tr in trs:
                ip = tr.xpath('./td[1]/text()')[0].strip().replace(' ','')
                port = tr.xpath('./td[2]/text()')[0].strip().replace(' ','')
                scheme = tr.xpath('./td[4]/text()')[0].lower().strip().replace(' ','')
                # 拼接代理
                proxy = '%s://%s:%s' % (scheme, ip, port)
                yield proxy,ip,port,scheme

    def crawl_xiladaili(self):
        url = self.cfg.get('xila','url')
        types = self.cfg.get('xila','types').lstrip('[').rstrip(']').split(',')
        page_num = int(self.cfg.get('xila','page_num'))

        for type in types:
            for page in range(1,page_num):
                proxy_list_url = url.format(type,page)
                response_text = get_page(proxy_list_url)
                if response_text:
                    html = etree.HTML(response_text)
                    trs = html.xpath('//table/tbody/tr')
                    for tr in trs:
                        ip_port = tr.xpath('./td[1]/text()')[0]
                        ip,port = ip_port.split(':')
                        scheme_str = tr.xpath('./td[2]/text()')[0].lower()
                        scheme = 'https' if 'https' in scheme_str else 'http'
                        # 拼接代理
                        proxy = '%s://%s' % (scheme, ip_port)
                        yield proxy,ip,port,scheme




