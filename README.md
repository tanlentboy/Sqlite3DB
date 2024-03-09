# Sqlite3DB
Sqlite3 使用线程局部数据(Python 的 threading.local() 函数)实现每个线程都有自己的数据副本，而不是所有线程共享同一份数据。你可以使用这个函数来为每个线程创建自己的数据库连接。
