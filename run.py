from proxypool.scheduler import Scheduler
import sys
import io
from configparser import ConfigParser
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main(cfg):
    try:
        s = Scheduler(cfg)
        s.run()
    except Exception as e:
        print(e)
        main()


if __name__ == '__main__':
    cfg = ConfigParser()
    cfg.read('config.ini', encoding='utf-8')
    main(cfg)
