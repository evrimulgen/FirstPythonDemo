#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入SQLite驱动:
import sqlite3
import traceback

from VipType import *
from datetime import *
import UserUtil


class DbUtil:
	def open_conn(self):
		# 连接到SQLite数据库
		# 数据库文件是user.db
		# 如果文件不存在，会自动在当前目录创建:
		conn = sqlite3.connect('user.db',check_same_thread = False)
		return conn
	
	def open_cursor(self,conn):
		# 创建一个Cursor:
		cursor = conn.cursor()
		# 执行一条SQL语句，创建user表:
		cursor.execute('create table IF NOT EXISTS user (\
						name varchar(200) NOT NULL, \
						phone_num varchar(200) NOT NULL, \
						md5 varchar(200) NOT NULL, \
						unique_mark varchar(200),\
						register_time varchar(200),\
						balance_times INT,\
						vip_type INT,\
						status bool,\
						PRIMARY KEY (md5)) ')
		return cursor
	
	def close_db(self,conn,cursor):
		# # 如果cursor变量已定义
		# if 'cursor' in dir():
		# 关闭Cursor:
		cursor.close()
		# 提交事务:
		conn.commit()
		# 关闭Connection:
		conn.close()	
	
	def select_user_info(self,md5):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute("select * from user where md5 = ? ",(md5,))
		results = cursor.fetchone()
		self.close_db(conn,cursor)
		return results
		
	# 当用户绑定设备时，设置激活时间
	def update_unique_mark(self,md5,unique_mark):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute("UPDATE user SET unique_mark = ?,register_time = ? WHERE md5 = ?",(unique_mark,datetime.now(),md5))
		self.close_db(conn,cursor)
	
	# 使用分裂标题接口时，使用次数－1
	def update_use_times(self,md5,use_times):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute("UPDATE user SET balance_times = ? WHERE md5 = ?",(use_times,md5))
		self.close_db(conn,cursor)

	# 新增用户
	def insert(self,name,phone_num,vip_type_str):
		vip_type = int(vip_type_str)
		rows = 0
		use_times = UserUtil.get_use_times_by_value(vip_type)
		md5 = UserUtil.get_md5(name,phone_num)
		if md5 == '':
			return rows
		try:
			conn = self.open_conn()
			cursor = self.open_cursor(conn)
			# 继续执行一条SQL语句，插入一条记录:
			cursor.execute("insert into user \
				(name,phone_num,md5,unique_mark,register_time,balance_times,vip_type,status)\
				values (?,?,?,?,?,?,?,?)",\
				(name,phone_num,md5,'','',use_times,vip_type,True))
			rows = conn.total_changes
			self.close_db(conn,cursor)
		except sqlite3.IntegrityError as e:
			print(e)
			pass
		except sqlite3.Error as e:
			print(e)
			pass
		finally:
			pass
		return rows

	def get_all(self):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute('select * from user')
		results = cursor.fetchall()
		self.close_db(conn,cursor)
		return results[::-1]

	# def get_last_one(self):
	# 	conn = self.open_conn()
	# 	cursor = self.open_cursor(conn)

	# 	cursor.execute('select rowid from user')
	# 	print(cursor.fetchone())
	# 	cursor.execute('select last_insert_rowid()')
	# 	print(cursor.fetchone())
	# 	print(cursor.lastrowid)
	# 	self.close_db(conn,cursor)	

	def get_count(self,list_all):
		return len(list_all)

# if __name__ == "__main__":
# 	db = DbUtil()	
# 	db.get_last_one()
# 	# db.insert("龚文1",'15010652066',VipType.forever)
# 	# db.insert("龚文2",'15010652066',VipType.month)
# 	# db.insert("龚文3",'15010652066',VipType.quarter)
# 	# db.insert("龚文4",'15010652066',VipType.half_year)
	
# 	print(str(db.insert("龚二111文",'18201077391',VipType.year)))

	
	########################################################################################################################
	
	
	
	
	
	
	