from flask import Flask

from proxypool.db_utils import Mysql_DB

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    mysql_db = Mysql_DB()
    return mysql_db

@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    mysql_db = get_conn()
    id,ip,port,scheme,score = mysql_db.get_one_proxy()
    # 拼接代理
    proxy = '%s://%s:%s' % (scheme, ip, port)
    return proxy

@app.route('/list')
def get_proxy_list():
    """
    Get a proxy
    :return: 随机代理
    """
    mysql_db = get_conn()
    proxy_list = {}
    res = mysql_db.get_proxies()
    for index,(id,ip,port,scheme,score) in enumerate(res):

        # 拼接代理
        proxy = '%s://%s:%s' % (scheme, ip, port)
        proxy_list[index+1] = proxy
    return proxy_list

@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    mysql_db = get_conn()
    return str(mysql_db.count())


if __name__ == '__main__':
    app.run("127.0.0.1",5555)
