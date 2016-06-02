#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
from __future__ import division, unicode_literals

import os
import sys
import fcntl
import shelve
import functools

PY2 = (sys.version_info[0] == 2)
PY3 = (sys.version_info[0] == 3)

if PY2:
    str = unicode

    reload(sys)
    sys.setdefaultencoding('utf-8')

__all__ = ["ShelveDB"]

def atomic_rw(mode):
    '''装饰器，保证数据库的原子操作

    参数 mode 用于指定对数据库的查询('r')或者增删改('w')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            assert mode in ('r', 'w')
            fobj = open(self.dbname, 'a')
            fcntl.flock(fobj, fcntl.LOCK_EX)
            self.shelf = shelve.open(self.dbname, mode)

            def closeout():
                self.shelf.close()
                self.shelf = None
                fcntl.flock(fobj, fcntl.LOCK_UN)
                fobj.close()

            try:
                ret = func(*args, **kwargs)
            except KeyError as e:
                closeout()
                raise KeyError(e)
            except ValueError as e:
                closeout()
                raise KeyError(e)
            except Exception as e:
                closeout()
                class Error(Exception):
                    pass
                raise Error(e)

            closeout()
            return ret
        return wrapper
    return decorator

class ShelveDB(object):
    '''利用 shelve 模块实现一个简单的基于文件的数据库

    Python 中的 shelve 模块，可以提供一些简单的数据操
    作。在 shelve 模块中，key 必须为字符串，而值可以是
    python 所支持的数据类型。

    Example:

        shelf['a'] = 'a'
        shelf['c'] = [11, 234, 'a']
        shelf['t'] = ('1', '2', '3')
        shelf['d'] = {'a':'2', 'name':'Hongte' }
        shelf['b'] = 'b'
        shelf['i'] = 23

    由于 shelve 每次 open 会将数据全部载入内存，并且
    在 close 时将数据写入文件，并释放内存，为了让数据
    库能够实现同步，本类没有实现迭代器对象的返回。

    所以，不建议用本类实现的数据库存储大量数据，实际上
    shelve 本省也不适合存储大量数据。

    接口：

        ShelveDB.save(key, value)
        ShelveDB.delete(key)
        ShelveDB.deleteall()
        ShelveDB.fetchone(key)
        ShelveDB.fetchall()
        ShelveDB.fetchkeys()
        ShelveDB.fetchvalues()
        ShelveDB.has_key(key)
    '''
    def __init__(self, dbname="test.dat"):
        self.dbname = dbname
        self.shelf = None

        if not os.path.isfile(self.dbname):
            shelve.open(self.dbname, 'n').close()

    @atomic_rw('w')
    def save(self, key, value):
        '''保存数据

        如果 key 不存在则存入，如果 key 存在则更新

        不支持重复的数据
        '''
        self.__check_key(key)
        self.__check_value(value)
        self.shelf[key] = value
        return True

    @atomic_rw('w')
    def delete(self, key):
        '''删除某个数据'''
        self.__check_key(key)
        keys = self.shelf.keys() if PY3 else self.shelf.iterkeys()
        if key not in keys:
            return False
        del self.shelf[key]
        return True

    @atomic_rw('w')
    def deleteall(self):
        '''删除所有数据'''
        self.shelf.clear()
        return True

    @atomic_rw('r')
    def fetchone(self, key):
        '''获取某个数据'''
        self.__check_key(key)
        keys = self.shelf.keys() if PY3 else self.shelf.iterkeys()
        if key not in keys:
            return None
        return self.shelf[key]

    @atomic_rw('r')
    def fetchall(self):
        '''获取所有数据'''
        data = {}
        items = self.shelf.items() if PY3 else self.shelf.iteritems()
        for key, value in items:
            data[key] = value
        return data

    @atomic_rw('r')
    def fetchkeys(self):
        '''获取所有的键'''
        if PY2:
            return self.shelf.keys()
        elif PY3:
            return list(self.shelf.keys())

    @atomic_rw('r')
    def fetchvalues(self):
        '''获取所有的值'''
        if PY2:
            return self.shelf.values()
        elif PY3:
            return list(self.shelf.values())

    @atomic_rw('r')
    def has_key(self, key):
        '''判断数据库中是否存在该键'''
        self.__check_key(key)
        if PY2:
            return self.shelf.has_key(key)
        elif PY3:
            return key in self.shelf.keys()

    @staticmethod
    def __check_key(key):
        if PY2 and isinstance(key, basestring):
            key = key if isinstance(key, unicode) else unicode(key)
        if not isinstance(key, str):
            raise KeyError("Key must be a string.")
        if key is None:
            raise KeyError("Key can't be None.")

    @staticmethod
    def __check_value(value):
        if value is None:
            raise ValueError("Value can't be None.")

if __name__ == "__main__":
    pass
