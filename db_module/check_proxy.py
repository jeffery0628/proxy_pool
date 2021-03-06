# -*- coding: utf-8 -*-
from configparser import ConfigParser
import requests
import time
from db_module.db_utils import Mysql_DB

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
                val_url = self.cfg.get('proxy-setting', 'val_url')
                response = requests.get(val_url, proxies={scheme: proxy})
                requests.session().close()
                # time.sleep(3)
                if response.status_code == 200:
                    cur_score = self.mysql_db.increase(ip)
                    print('代理：'+ip+' ip有效，原始分值为：'+str(score)+'\t + 5 分\t'+',现在分值为：'+str(cur_score))
                else:
                    # 无效代理减10分
                    cur_score = self.mysql_db.decrease(ip)
                    print('代理：'+ip+' ip失效，原始分值为：'+str(score)+'\t - 10 分\t'+',现在分值为：'+str(cur_score))
                response.close()
            except Exception as e:

                # 无效代理减10分
                cur_score = self.mysql_db.decrease(ip)
                print('代理：'+ip+' 失效，原始分值为：'+str(score)+'\t - 10 分\t'+',现在分值为：'+str(cur_score))


if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('../config.ini',encoding='utf-8')
    checker = Checker(cfg)
    while True:

        # 检查删除失效proxy
        checker.run()

        print('this loop check finished')
        time.sleep(300)

    connect.close()