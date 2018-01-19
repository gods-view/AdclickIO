#! /usr/bin/env	python2
# encoding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from configure import config
import redis
from log import Log


class RedisDB():
    def __init__(self, db_conf=None, open_log=False):
        if db_conf == None:
            self.db_conf = 'redis'
        else:
            self.db_conf = db_conf

        if open_log == True:
            self.error_log = Log('logs/resource_error.log')

        self.connect()

    def connect(self):
        try:
            auth = config.get(self.db_conf, 'auth')
            if auth == '':
                self.client = redis.StrictRedis(host=config.get(self.db_conf, 'host'),
                                                port=config.getint(self.db_conf, 'port'),
                                                db=int(config.getint(self.db_conf, 'db')))
            else:
                self.client = redis.StrictRedis(host=config.get(self.db_conf, 'host'),
                                                port=config.getint(self.db_conf, 'port'), password=auth,
                                                db=int(config.getint(self.db_conf, 'db')))
        except Exception, e:
            self.error_log.error("connect redis error! %s" % e.message)
            sys.exit()

    def dispose(self):
        self.client.connection_pool.disconnect()

    def close(self):
        self.client.connection_pool.disconnect()

    def checkConn(self):
        if not self.client.ping():
            self.connect()

    def __enter__(self):
        try:
            return self
        except IOError, e:
            print 'Error %s' % str(e)
            # return None

    def __exit__(self, type, value, traceback):
        self.dispose()

    def __del__(self):
        if hasattr(self, "error_log") == True:
            if hasattr(self.error_log, "close") == True:
                self.error_log.close()
