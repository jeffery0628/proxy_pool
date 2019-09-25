# proxy_pool

1. check_proxy.py：用于检测mysql数据库中的ip是否可用，如果可用，则将该代理ip的分值+5，最多分值可以加到100，如果不可用，代理ip的分值每次-10，当代理ip的分值为0的时候，从mysql数据控中删除该代理ip。
2. db_utils.py: 主要是对代理进行mysql增删改的函数
3. crawler.py : 以crawl开头的函数是爬取代理网站（规则）的具体实现，
4. getter.py : 主要是调用crawler.py 中以crawl开头的函数，对各个代理网站的ip进行爬取。
5. webapi.py : 主要是以网站的形式，给用户提供代理ip。比如：通过在浏览器输入：127.0.0.1:5000/random，会返回一个分值相对较高的代理 （分值越高，代理的可用性越强）。也可以运行在服务器上，给其他用于提供代理
6. utils.py: 主要是用于获取页面源码，获取页面中ip的规则写在crawler.py中
7. scheduler.py : 使用三个线程跑getter.py(获取)，check_proxy.py(检查代理)，webapi.py(提供代理)。也可以分别运行getter.py,check_proxy.py,webapi.py.
8. config.ini:整个项目的配置文件：

其余的文档，有时间在写。

