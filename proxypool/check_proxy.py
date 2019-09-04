# -*- coding: utf-8 -*-
from configparser import ConfigParser
import requests
import time
from proxypool.db_utils import Mysql_DB

class Checker():
    def __init__(self,cfg):
        self.mysql_db = Mysql_DB(cfg)
        self.cfg = cfg

    def run(self):

        # 查询数据库中存在的proxy
        proxies = self.mysql_db.get_proxies(0,100)
        print('数据库中代理ip的数量：'+str(len(proxies)))
        for id,ip,port,scheme,score in proxies:
            # 拼接代理
            proxy = '%s://%s:%s' % (scheme, ip, port)
            try:
                # 验证代理是否有效
                val_url = self.cfg.get('url', 'val_url')
                response = requests.get(val_url, proxies={scheme: proxy})
                if response.status_code == 200:
                    cur_score = self.mysql_db.increase(ip)
                    print(ip+'\t ip有效，原始分值为：'+str(score)+'\t + 5 分\t'+',现在分值为：'+str(cur_score))
                else:
                    # 无效代理减10分
                    cur_score = self.mysql_db.decrease(ip)
                    print(ip+'\t ip失效，原始分值为：'+str(score)+'\t - 10 分\t'+',现在分值为：'+str(cur_score))
            except Exception as e:
                print(e.args)
                # 无效代理减10分
                cur_score = self.mysql_db.decrease(ip)
                print(ip+'\t ip失效，原始分值为：'+str(score)+'\t - 10 分\t'+',现在分值为：'+str(cur_score))


# if __name__ == '__main__':
#     cfg = ConfigParser()
#     cfg.read('../config.ini',encoding='utf-8')
#     mysql_db = Mysql_DB(cfg)
#     checker = Checker(mysql_db,cfg)
#     while True:
#
#         # 检查删除失效proxy
#         checker.run()
#
#         print('this loop check finished')
#         # time.sleep(60)
#
#     connect.close()