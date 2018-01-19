#! /usr/bin/env	python2
# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from configure import config
from pymongo import MongoClient
from core.log import Log

class Mongo():
	client = None
	def __init__(self,db_conf=None, log=None):
		try:
			self.client = MongoClient(config.get(db_conf,'dns'))
		except Exception,e:
			if isinstance(log, Log):
				log.info("connect mongo error "+e.message);
			else:
				print e
			#sys.exit();
	
	def ping(self):
		if self.client is not None:
			try:
				res = self.client.admin.command('ping')
				return True
			except:
				return False
		else:
			return False
	
	def dispose(self):
		self.client.close()
			
	def close(self):
		self.dispose()

	def __enter__(self):  
		try:  
			return self
		except IOError ,e:
			print 'Error %s' % str(e)
		#return None
	
	def __exit__(self, type, value, traceback): 
		self.dispose()