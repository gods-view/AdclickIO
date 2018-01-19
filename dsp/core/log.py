# encoding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import logging
from configure import config
from hashlib import md5


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


# @singleton
# 使用修饰器, 虽然优美, 但是达不到要求



# 实现以log_path为key的单例模式, 即一个log_path只会生成一个实例
class Log(object):
    _instance = dict();

    def __init__(self, log_path, is_stream=False):
        self.logger = logging.getLogger(log_path)
        self.logger.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(config.get('env', 'project_path') + log_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        if is_stream or config.get('env', 'debug') == '1':
            # 创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def __new__(cls, log_path, is_stream=False):
        if not cls._instance.has_key(log_path):
            orig = super(Log, cls)
            cls._instance[log_path] = orig.__new__(cls)
        return cls._instance[log_path]

    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def close(self):
        logging.shutdown()
