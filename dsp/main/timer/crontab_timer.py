#! /usr/bin/env python2
# encoding=utf-8
import os, sys

sys.path.insert(0, os.path.dirname(sys.path[0]) + '/../')
reload(sys)
sys.setdefaultencoding('utf8')
from core.configure import config
from module.mgid import Mgid


def _main():
    print Mgid().login()


if __name__ == '__main__':
    _main()
