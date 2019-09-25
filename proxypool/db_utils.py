import pymysql
import random
from configparser import ConfigParser

class Mysql_DB():
    def __init__(self,cfg):
        self.cfg = cfg
        self.cfg.read('./config.ini',encoding='utf-8')
        # 读取数据库相关配置
        db = self.cfg.get('mysql_data', 'db_name')
        host = self.cfg.get('mysql_data', 'host')
        mysql_port = self.cfg.get('mysql_data', 'port')
        user = self.cfg.get('mysql_data', 'user')
        passwd = self.cfg.get('mysql_data', 'passwd')
        self.low_score = int(self.cfg.get('proxy-setting','low_score'))
        self.heigh_score = int(self.cfg.get('proxy-setting','heigh_score'))
        # 连接mysql数据库
        self.connect = pymysql.Connection(
            host=host,
            port=int(mysql_port),
            db=db,
            user=user,
            passwd=passwd,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

        # 操作的数据库的表名
        self.table_name = self.cfg.get('mysql_data', 'table_name')


    # 向数据库中插入一条ip，如果该ip存在，则不进行插入
    def insert_ip(self,ip,port,scheme,score):
        query_sql = """select * from %s where ip = '%s'""" %(self.table_name,ip)
        self.cursor.execute(query_sql)
        res = self.cursor.fetchall()
        if len(res) > 0:
            print('数据库中存在ip：'+ip+'  不进行插入')
            self.connect.commit()
            return 0
        insert_sql = """insert into %s (ip,port,scheme,score) values('%s','%s','%s','%s')""" %(self.table_name,ip,port,scheme,score)
        self.cursor.execute(insert_sql)
        print('向数据库中插入ip：'+ip)
        self.connect.commit()
        return 1

    # 从数据库中删除该代理
    def delete_ip(self,ip):
        del_sql = """delete from %s where ip = '%s' """ % (self.table_name, ip)
        self.cursor.execute(del_sql)
        self.connect.commit()


    # 清空表中数据
    def clear_table(self):
        clear_sql = """truncate table %s""" %(self.table_name)
        self.cursor.execute(clear_sql)
        self.connect.commit()

    # 创建表
    def create_table(self):
        create_table_sql = """create table if not exists %s (id int NOT NULL AUTO_INCREMENT,ip varchar(20),port varchar(10),scheme varchar(10),score int ,PRIMARY KEY (id))""" %self.table_name
        self.cursor.execute(create_table_sql)
        self.connect.commit()

    # 获取分数值在min_score~max_score之间的代理ip,并进行降序排序
    def get_proxies(self,min_score=50,max_score=100):
        query_sql = """select * from %s where score between '%s' and '%s' order by score desc """ %(self.table_name,min_score,max_score)
        self.cursor.execute(query_sql)
        proxies_list = self.cursor.fetchall()
        self.connect.commit()
        return proxies_list

    # 对于可用的ip，每次增加5分值
    def increase(self,ip):
        update_sql = """update %s a inner join (select * from %s where ip like '%s' ) b on a.id = b.id set a.score = b.score + 5 """ %(self.table_name,self.table_name,ip)
        self.cursor.execute(update_sql)
        query_sql = """select score from %s where ip like '%s'""" %(self.table_name,ip)
        self.cursor.execute(query_sql)
        score = self.cursor.fetchone()[0]
        if score >= 100:
            reupdate_sql = """update %s set score = 100 where ip = '%s'""" %(self.table_name,ip)
            self.cursor.execute(reupdate_sql)
            self.connect.commit()
            return 100
        self.connect.commit()
        return score

    # 对于连接失败的ip，每次减10分
    def decrease(self,ip):
        update_sql = """update %s a inner join (select * from %s where ip like '%s' ) b on a.id = b.id set a.score = b.score - 10 """ %(self.table_name,self.table_name,ip)
        self.cursor.execute(update_sql)
        query_sql = """select score from %s where ip like '%s'""" %(self.table_name,ip)
        self.cursor.execute(query_sql)
        score = self.cursor.fetchone()[0]
        # 如果小于0 就进行删除
        if score < 0:
            del_sql = """delete from %s where ip like '%s' """ % (self.table_name, ip)
            print(ip+'\t 分值为： '+str(score)+' 从数据库中删除该ip')
            self.cursor.execute(del_sql)
            self.connect.commit()
            return 0
        self.connect.commit()
        return score

    # 统计数据库中代理个数
    def count(self):
        query_sql = """SELECT COUNT(*) from %s""" %(self.table_name)
        self.cursor.execute(query_sql)
        count = self.cursor.fetchone()
        return count[0]

    # 随机获取一个可以使用的代理
    def get_one_proxy(self):
        proxy_list = self.get_proxies(self.low_score,self.heigh_score)
        return random.choice(proxy_list)


if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('../config.ini',encoding='utf-8')
    mysql_db = Mysql_DB(cfg)
    mysql_db.create_table()

