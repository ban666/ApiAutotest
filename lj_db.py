# -*- coding: utf-8 -*-
__author__ = 'liaoben'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lj_models import *

class Db(object):

    def __new__(cls,dbname='house',host='localhost',username='root',password='123456'):
        DB_CONNECT_STRING = 'mysql+mysqldb://%s:%s@%s/%s?charset=utf8'%(username,password,host,dbname)
        engine = create_engine(DB_CONNECT_STRING)
        DB_Session = sessionmaker(bind=engine)
        session = DB_Session()
        return session

if __name__ == '__main__':
    pass