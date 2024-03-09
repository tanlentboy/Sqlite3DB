# Sqlite3DB
Sqlite3 使用线程局部数据(Python 的 threading.local() 函数)实现每个线程都有自己的数据副本，而不是所有线程共享同一份数据。你可以使用这个函数来为每个线程创建自己的数据库连接。

#初始化数据库

db = SqliteDB("sqlite3.db")

sql = "CREATE TABLE bob (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, bob VARCHAR, status VARCHAR, title VARCHAR, cover VARCHAR, stars double, lreviewdate VARCHAR, description VARCHAR, url VARCHAR, atime timestamp NULL DEFAULT NULL, mtime timestamp NULL DEFAULT NULL, price double, flag INTEGER DEFAULT 0, reviewcount INTEGER DEFAULT 0)"

sql = "CREATE TABLE keyword (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, keyword VARCHAR, flag INTEGER DEFAULT 0, isrelate INTEGER DEFAULT 0, locked INTEGER DEFAULT 0, );"

sql = "CREATE TABLE pre_bob (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, bob VARCHAR, status VARCHAR, title VARCHAR, cover VARCHAR, stars double, lreviewdate VARCHAR, description VARCHAR, url VARCHAR, atime timestamp NULL DEFAULT NULL, mtime timestamp NULL DEFAULT NULL, price double, flag INTEGER DEFAULT 0, reviewcount INTEGER DEFAULT 0)"

res = db.createtb(sql=sql,table='bob')

print(res)

# insert测试
cs = db.insert(table="bob", bob=bob, title="标题"+str(random.randint(100,999)), stars=4.3)
print(cs)

# delete 测试
cs = db.delete(table="bob", where="id=6")
print(cs)

# update 测试
cs = db.update(table="bob", title="8888", stars=4.9, where="id=2")
print(cs)

# select 测试
cs = db.getAll(table="bob", where="1")
print(cs)
# 关闭数据库
db.close
