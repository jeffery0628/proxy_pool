import time
from multiprocessing import Process
from proxypool.getter import Getter
from proxypool.check_proxy import Checker
from configparser import ConfigParser
from proxypool.db_utils import Mysql_DB
from proxypool.webapi import app

class Scheduler():
    def __init__(self,cfg):
        self.cfg = cfg
        # self.mysql_db = Mysql_DB(self.cfg)


    def schedule_checker(self):
        """
        定时测试代理
        """
        checker_sleep_time = int(self.cfg.get('proxy-setting','check_sleep_time'))
        checker = Checker(self.cfg)
        while True:
            print('测试器开始运行')
            checker.run()
            time.sleep(checker_sleep_time)
    
    def schedule_getter(self):
        """
        定时获取代理
        """
        getter_sleep_time = int(self.cfg.get('proxy-setting', 'getter_sleep_time'))
        getter = Getter(self.cfg)
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(getter_sleep_time)
    
    def schedule_webapi(self):
        """
        开启API
        """
        api_host = self.cfg.get('proxy-setting','api_host')
        api_port = self.cfg.get('proxy-setting','api_port')
        app.run(host=api_host, port=api_port)
    
    def run(self):
        print('代理池开始运行')
        checker_enabled = self.cfg.get('proxy-setting','checker_enabled')
        getter_enabled = self.cfg.get('proxy-setting','getter_enabled')
        web_api_enabled = self.cfg.get('proxy-setting','web_api_enabled')
        if checker_enabled:
            checker_process = Process(target=self.schedule_checker)
            checker_process.start()
        
        if getter_enabled:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        
        if web_api_enabled:
            api_process = Process(target=self.schedule_webapi)
            api_process.start()
