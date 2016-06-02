#! /usr/bin/env python
# -*- coding: utf-8 -*-

# *************************************************************
#     Filename @  test_shelvedb.py
#       Author @  Huoty
#  Create date @  2016-06-02 10:19:33
#  Description @
# *************************************************************

from __future__ import print_function, absolute_import

import os
import sys

sys.path.append(os.path.dirname(__file__)+"/..")
from shelvedb import ShelveDB

def test():
    shdb = ShelveDB()
    print("-" * 30)
    print("All data: ", shdb.fetchall())
    print("-" * 30)
    print(shdb.save("one", range(10)))
    print(shdb.save("two", range(20)))
    print(shdb.save("three", {"a": 1, "b": 2}))
    print(shdb.save('a', 'a'))
    print(shdb.save('c', [11, 234, 'a']))
    print(shdb.save('t', ('1', '2', '3')))
    print(shdb.save('d', {'a':'2', 'name':'Huoty' }))
    print(shdb.save('b', 'b'))
    print(shdb.save('i', 23))
    print("-" * 30)
    print("All data: ", shdb.fetchall())
    print("-" * 30)
    print(shdb.delete("two"))
    print(shdb.fetchone("two"))
    print(shdb.fetchone("three"))
    print(shdb.fetchkeys())
    print(shdb.fetchvalues())
    print(shdb.has_key("one"))
    print(shdb.has_key("six"))
    print(shdb.deleteall())
    print("-" * 30)
    print("All data: ", shdb.fetchall())
    print("-" * 30)

# cmd :
#   python -m pytest test_shelvedb.py -s
#   or
#   python3 -m pytest test_shelvedb.py -s
