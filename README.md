ShelveDB
========

利用 shelve 模块实现一个简单的基于文件的键值数据库。Python 中的 shelve 模块，可以提供一些简单的数据操作。在 shelve 模块中，key 必须为字符串，而值可以是python 所支持的数据类型。

Example:

    shelf['a'] = 'a'
    shelf['c'] = [11, 234, 'a']
    shelf['t'] = ('1', '2', '3')
    shelf['d'] = {'a':'2', 'name':'Hongte' }
    shelf['b'] = 'b'
    shelf['i'] = 23

**注：**

由于 shelve 每次 open 会将数据全部载入内存，并且在 close 时将数据写入文件，并释放内存，为了让数据库能够实现同步，本类没有实现迭代器对象的返回。所以，不建议用本类实现的数据库存储大量数据，实际上shelve 本省也不适合存储大量数据。

## 接口说明

所有 key 参数都必须是字符串类型，否则会有 KeyError 异常.

#### ShelveDB.save(key, value)

保存数据。如果 key 不存在则存入，否则更新 key 对应的值。因此数据库不存放重复的值。

#### ShelveDB.delete(key)

删除 key 对应的数据。

#### ShelveDB.deleteall()

删除所有数据，即清空数据库。

#### ShelveDB.fetchone(key)

获取一条 key 对应的数据。

#### ShelveDB.fetchall()

获取数据库所有的数据。

#### ShelveDB.fetchkeys()

获取所有的键。

#### ShelveDB.fetchvalues()

获取所有的值。

#### ShelveDB.has_key(key)

判断数据库中是否存在 key。

## 兼容问题

本模块能够在 Python2 和 Python3 环境下使用，但是在 Python2 下创建的数据库由于存储协议的不同，在 Python3 中无法打开。这个问题暂时没有解决，但在 Python3 环境下创建的数据库在 Python2 环境下可以正常使用。
