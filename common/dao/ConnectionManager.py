#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
DB_LOCK = threading.RLock()
import os
import psycopg2
from psycopg2.pool import PersistentConnectionPool
from time import sleep
import json

config_cache = dict()
conn_pool = None

MAX_CONNECTIONS_IN_POOL = 1

connexion_map = dict()


class ConnectionManager(object):

    @staticmethod
    def _get_config_path():
        return os.path.dirname(__file__) + "/../../conf/databases.json"

    @staticmethod
    def get_config(database_config_name, path_to_conf_file=None):
        global config_cache
        if not config_cache.get(database_config_name):
            if path_to_conf_file is None:
                path_to_conf_file = ConnectionManager._get_config_path()

            with open(path_to_conf_file, "r", encoding="utf-8") as f:
                file_content = f.read()


            config_cache = json.loads(file_content)
        return config_cache[database_config_name]

    @staticmethod
    def get_connection(database_config_name, path_to_conf_file=None):
        global conn_pool, MAX_CONNECTIONS_IN_POOL

        if conn_pool is None:
            config = ConnectionManager.get_config(database_config_name, path_to_conf_file)

            conn_pool = PersistentConnectionPool(minconn=1, maxconn=MAX_CONNECTIONS_IN_POOL,
                                                 host=config['host'],
                                                 database=config['database'],
                                                 user=config['user'],
                                                 password=config['password'])
        got_connection = False
        while not got_connection:
            try:
                conn = conn_pool.getconn()
                #cur = conn.cursor(cursor_factory=cursor_type)
                got_connection = True
            except psycopg2.OperationalError as mess:
                print("OperationalError opening connexion : %s" % mess)
                sleep(1)
            except AttributeError as mess:
                print("AttributeError opening connexion : %s" % mess)
                sleep(1)
        return conn

    @staticmethod
    def release_connection(conn):
        conn_pool.putconn(conn)

