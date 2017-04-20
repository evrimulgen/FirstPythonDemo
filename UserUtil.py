#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback

# import hashlib
from DateUtil import *
from DbUtil import *

VIP_USE_TIMES = (5, 80, 600, 1300, 0)
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


# def get_use_times(vip_type):
# 	if vip_type in VipType:
# 		return VIP_USE_TIMES[vip_type.value]
# 	else:
# 		return 0

def get_use_times_by_value(vip_type):
	if vip_type < VipType.trial.value or vip_type > VipType.forever.value:
		return 0
	return VIP_USE_TIMES[vip_type]


def get_vip_type_desc_by_value(vip_type):
	if vip_type == VipType.trial.value:
		return "试用会员(2天)"
	elif vip_type == VipType.month.value:
		return '月费会员'
	elif vip_type == VipType.half_year.value:
		return '半年会员'
	elif vip_type == VipType.year.value:
		return '年费会员'
	elif vip_type == VipType.forever.value:
		return '永久会员'
	else:
		return '异常会员'


def get_ok_msg():
	result_ok = {'status': True}
	return result_ok


def get_err_msg(code):
	result_err = {'status': False}
	result_err['err_code'] = code
	err_msg = ''
	if code == 0:
		err_msg = '用户名不能为空'
	elif code == 1:  # 设备ID为空
		err_msg = '设备异常'
	elif code == 2:
		err_msg = '用户名不存在'
	elif code == 3:
		err_msg = '该软件只能绑定一台设备'
	elif code == 4:
		err_msg = '使用次数已经用完'
	elif code == 5:
		err_msg = '会员已到期'
	elif code == 6:
		err_msg = '添加新用户失败'
	else:
		err_msg == '非法状态'
	result_err['err_msg'] = err_msg
	return result_err


# 校验用户信息
def check_user_info(account, unique_mark, is_count_search_times):
	result_msg = get_ok_msg()
	if account is None or account == '':
		result_msg = get_err_msg(0)
	elif unique_mark is None or unique_mark == '':
		result_msg = get_err_msg(1)
	else:
		try:
			results = db.select_user_info(account)
			if results != None:
				db_unique_mark = results[1]
				register_time = results[2]
				use_times = results[3]
				vip_type = results[4]

				if register_time is not None and register_time != '':
					result_msg['dateline'] = date_util.getDateline(register_time, vip_type)
				if vip_type == VipType.forever.value:
					result_msg['balance_times'] = '无限次'
				else:
					result_msg['balance_times'] = str(use_times) + '次'
				result_msg['vip_type'] = get_vip_type_desc_by_value(vip_type)

				if db_unique_mark is None or db_unique_mark == '':
					result_msg['dateline'] = date_util.getDateline(db.update_unique_mark(account, unique_mark),
					                                               vip_type)
				elif unique_mark == db_unique_mark:
					if vip_type != VipType.forever.value:
						if date_util.isVipValid(register_time, vip_type):
							if use_times <= 0:
								result_msg = get_err_msg(4)
							elif is_count_search_times:
								use_times = use_times - 1
								db.update_use_times(account, use_times)
								result_msg['dateline'] = date_util.getDateline(register_time, vip_type)
								result_msg['balance_times'] = str(use_times) + '次'
						else:
							result_msg = get_err_msg(5)
					else:
						result_msg['dateline'] = '永久'
						result_msg['balance_times'] = '无限次'
				else:
					result_msg = get_err_msg(3)
			else:
				result_msg = get_err_msg(2)
		except sqlite3.Error as e:
			print(str(e))
			print('traceback.print_exc():', traceback.print_exc())
			result_msg = get_err_msg(-1)
	return result_msg


def get_all_user_info():
	return db.get_all()


def get_last_user_info():
	return db.get_last_one()


def add_new_user(account, user_name, vip_type):
	rows = db.insert(account, user_name, vip_type)
	return rows


def delete_one_user(account):
	rows = db.delete_one_user(account)
	return rows


def update_one_user(account, user_name, use_times, vip_type):
	rows = db.update_one_user(account, user_name, use_times, vip_type)
	return rows

# def get_md5(name,phone_num):
# 	if isinstance(name,str) and isinstance(phone_num,str) and name != '' and phone_num != '':
# 		result = name + phone_num
# 		result_encode = result.encode('utf-8')
# 		# print(result,result_encode)
# 		m = hashlib.md5()
# 		m.update(result_encode)
# 		return m.hexdigest()
# 	else:
# 		return ''
