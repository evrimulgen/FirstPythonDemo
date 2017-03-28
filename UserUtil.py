#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from VipType import * 
from DbUtil import *

import sqlite3
import traceback
from DateUtil import *

VIP_USE_TIMES = (3,10,21,43,0)
# 月会员3次
# 季度10次
# 半年会员21次
# 年会员43次
# 永久会员
db = DbUtil()
date_util = DateUtil()

def is_use_forever(vip_type):
	if vip_type == VipType.forever:
		return True
	else:
		return False

def get_use_times(vip_type):
	if vip_type in VipType:
		return VIP_USE_TIMES[vip_type.value]
	else:
		return 0

def get_ok_msg():
	result_ok = {'status':True}
	return result_ok

def get_err_msg(code):
	result_err = {'status':False}
	result_err['err_code'] = code
	err_msg = ''
	if code == 0:
		err_msg = '用户名不能为空'
	elif code == 1:#设备ID为空
		err_msg = '设备异常'
	elif code == 2:
		err_msg = '用户名不存在'
	elif code == 3:
		err_msg = '该软件只能绑定一台设备'
	elif code == 4:
		err_msg = '每月次数已经用完'
	elif code == 5:
		err_msg = '会员已到期'
	else:
		err_msg == '非法状态'
	result_err['err_msg'] = err_msg
	return result_err

# 返回字典
def get_user_info(name,unique_mark,is_count_search_times):
	result_msg = get_ok_msg()
	if name is None or name == '':
		result_msg = get_err_msg(0)
	elif unique_mark is None or unique_mark == '':
		result_msg = get_err_msg(1)
	else:
		try:
			results = db.select_user_info(name)
			if results != None:
				db_unique_mark = results[1] 
				register_time = results[2]
				use_times = results[3]
				vip_type = results[4]
				if db_unique_mark == '':
					db.update_unique_mark(name,unique_mark)
				elif unique_mark == db_unique_mark:
					if vip_type != VipType.forever.value:
						if date_util.isVipValid(register_time,vip_type):
							if use_times <= 0:
								result_msg = get_err_msg(4)
							elif is_count_search_times:
								use_times = use_times - 1
								db.update_use_times(name,use_times)
						else:
							result_msg = get_err_msg(5)
				else:
					result_msg = get_err_msg(3)
			else:
				result_msg = get_err_msg(2)
		except sqlite3.Error as e:
			print(str(e))
			print ('traceback.print_exc():',traceback.print_exc())
			result_msg = get_err_msg(-1)
	return result_msg