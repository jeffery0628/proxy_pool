from proxypool.crawler import Crawler
import sys
from proxypool.db_utils import Mysql_DB
import requests
class Getter():
    def __init__(self,cfg):
        self.cfg = cfg
        self.mysql_db = Mysql_DB(cfg)
        self.crawler = Crawler(cfg)
    
    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        pool_upper_threshold = int(self.cfg.get('proxy-setting','pool_upper_threshold'))
        if self.mysql_db.count() >= pool_upper_threshold:
            return True
        else:
            return False
    
    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                for (proxy,ip,port,scheme) in proxies:
                    initial_score = self.cfg.get('proxy-setting','initial_score')
                    # 向数据库插入之前，进行一次校验，通过的ip才能插入数据库
                    val_url = self.cfg.get('proxy-setting','val_url')
                    try:
                        response = requests.get(val_url,proxies={scheme:proxy})
                        if response.status_code == 200:
                            self.mysql_db.insert_ip(ip,port,scheme,initial_score)
                    except Exception as e:
                        print(e.args)


# if __name__ == '__main__':
#     cfg = ConfigParser()
#     cfg.read('../config.ini', encoding='utf-8')
#     mysql_db = Mysql_DB(cfg)
#     getter = Getter(mysql_db,cfg)
#     getter.run()