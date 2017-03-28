#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入SQLite驱动:
import sqlite3
import time
import traceback

from VipType import *
from enum import Enum
# from datetime import *
from UserUtil import *


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
						unique_mark varchar(200),\
						register_time varchar(200),\
						balance_times INT,\
						vip_type INT,\
						status bool,\
						PRIMARY KEY (name)) ')
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
	
	def select_user_info(self,name):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute("select * from user  where name = ? ",(name,))
		time.sleep(5)
		results = cursor.fetchone()
		self.close_db(conn,cursor)
		return results
		
	def update_unique_mark(self,name,unique_mark):
		conn = self.open_conn()
		cursor = self.open_cursor(conn)
		cursor.execute("UPDATE user SET unique_mark = ? WHERE name = ?",(unique_mark,name))
		self.close_db(conn,cursor)
	
	def update_use_times(self,name,use_times):
		try:
			conn = self.open_conn()
			cursor = self.open_cursor(conn)
			cursor.execute("UPDATE user SET balance_times = ? WHERE name = ?",(use_times,name))
			print(use_times)
			self.close_db(conn,cursor)
		except sqlite3.Error as e:
			print(str(e))
			print ('traceback.print_exc():',traceback.print_exc())

	# def insert(self,name,unique_mark,vip_type):
	# 	use_times = get_use_times(vip_type)
	# 	print(use_times)
	# 	conn = self.open_conn()
	# 	cursor = self.open_cursor(conn)
	# 	# 继续执行一条SQL语句，插入一条记录:
	# 	cursor.execute("insert into user (name, unique_mark,register_time,balance_times,vip_type,status) values (?,?,?,?,?,?)",(name,unique_mark,datetime.now(),use_times,vip_type.value,True))
	# 	self.close_db(conn,cursor)

# if __name__ == "__main__":
# 	db = DbUtil()	
# 	db.insert("龚文1",'dd',VipType.month)
# 	db.insert("龚文3",'dd',VipType.quarter)
# 	db.insert("龚文4",'dd',VipType.half_year)
# 	db.insert("龚文5",'dd',VipType.year)
	
	########################################################################################################################
	# def get_all():
	# 	cursor.execute('select * from user')
	# 	return cursor.fetchall()
	
	# def get_count(list_all):
	# 	return len(list_all)
	
	
	
	
	
	