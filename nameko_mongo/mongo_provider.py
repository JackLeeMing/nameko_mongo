# -*- coding:utf-8 -*-
from nameko.extensions import DependencyProvider
from nameko.exceptions import safe_for_serialization
from weakref import WeakKeyDictionary
from types import ModuleType
from mongo_util import MongoIns
# nameko run service --broker amqp://guest:guest@192.168.111.31
# nameko shell --broker amqp://guest:guest@192.168.111.31

class NamekoMongoIns(DependencyProvider):
    def __init__(self,project, host=None, dbname=None):
        self.host = host
        self.dbname = dbname
        self.project = project

    def setup(self):
        debug = self.container.config.get('TEST', True)
        db_config = self.container.config.get('MONGO_CONFIG')
        if db_config:
            if debug:
                DB_NAME = db_config['Test'][self.project]['DB_NAME']
                DB_HOST = db_config['Test'][self.project]['DB_HOST']
            else:
                DB_NAME = db_config['Release'][self.project]['DB_NAME']
                DB_HOST = db_config['Release'][self.project]['DB_HOST']
            self.dbname = DB_NAME
            self.host = DB_HOST

        self.client = MongoIns(host=self.host, dbname=self.dbname)


    def start(self):
        pass

    def stop(self):
        self.client = None
        pass

    def kill(self):
        self.client = None
        pass

    def get_dependency(self, worker_ctx):
        return self.client




