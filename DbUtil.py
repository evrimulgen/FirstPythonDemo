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
						account varchar(200) NOT NULL, \
						unique_mark varchar(200),\
						register_time varchar(200),\
						balance_times INT,\
						vip_type INT,\
						status bool,\
						PRIMARY KEY (account)) ')
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
	
	def select_user_info(self,account):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute("select * from user where account = ? ",(account,))
		results = cursor.fetchone()
		self.close_db(conn,cursor)
		return results
		
	# 当用户绑定设备时，设置激活时间
	def update_unique_mark(self,account,unique_mark):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute("UPDATE user SET unique_mark = ?,register_time = ? WHERE account = ?",(unique_mark,datetime.now(),account))
		self.close_db(conn,cursor)
	
	# 使用分裂标题接口时，使用次数－1
	def update_use_times(self,account,use_times):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute("UPDATE user SET balance_times = ? WHERE account = ?",(use_times,account))
		self.close_db(conn,cursor)

	# 新增用户
	def insert(self,account,vip_type_str):
		vip_type = int(vip_type_str)
		rows = 0
		use_times = UserUtil.get_use_times_by_value(vip_type)
		try:
			conn = self.open_conn()
			cursor = self.open_cursor(conn)
			# 继续执行一条SQL语句，插入一条记录:
			cursor.execute("insert into user \
				(account,unique_mark,register_time,balance_times,vip_type,status)\
				values (?,?,?,?,?,?)",\
				(account,'','',use_times,vip_type,True))
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

	# 删除用户
	def delete_one_user(self,account):
		rows = 0
		try:
			conn = self.open_conn()
			cursor = self.open_cursor(conn)
			# 继续执行一条SQL语句，删除一条记录:
			cursor.execute("delete from user where account = ? " ,(account, ))
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

	def update_one_user(self,account,use_times,vip_type):
		rows = 0
		try:
			conn = self.open_conn()
			cursor = self.open_cursor(conn)
			cursor.execute("UPDATE user SET balance_times = ?,vip_type = ? WHERE account = ?",(use_times,vip_type,account))
			rows = conn.total_changes
			self.close_db(conn,cursor)
		except Exception as e:
			print(e)
		return rows

	def get_all(self):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute('select * from user')
		results = cursor.fetchall()
		self.close_db(conn,cursor)
		return results[::-1]

	def get_last_one(self):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute('select * from user order by rowid desc limit 1')
		results = cursor.fetchone()
		self.close_db(conn,cursor)
		return results

	def get_count(self,list_all):
		return len(list_all)

# if __name__ == "__main__":
# 	db = DbUtil()	
# 	db.get_last_one()
	
	
	
	
	
	
	