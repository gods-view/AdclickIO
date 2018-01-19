#! /usr/bin/env	python2
# encoding=utf-8
import sys
from imp import reload
reload(sys)
# sys.setdefaultencoding('utf8')

import os
import configparser


def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


common_file = cur_file_dir() + '/conf/common.ini'
if not os.path.exists(common_file):
    print('can not found %s file!' % common_file)
    sys.exit()

base_file = cur_file_dir() + '/conf/base.ini'
if not os.path.exists(base_file):
    print('can not found %s file!' % base_file)
    sys.exit()

conf_file = cur_file_dir() + '/conf/config.ini'
if not os.path.exists(conf_file):
    print('can not found %s file!' % conf_file)
    sys.exit()

resource_path = cur_file_dir() + '/resource'

config = configparser.ConfigParser()
config.read(common_file)
config.read(base_file)
config.read(conf_file)
