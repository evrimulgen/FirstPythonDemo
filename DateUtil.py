#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# http://dateutil.readthedocs.io/en/stable/examples.html

from datetime import *
from dateutil.relativedelta import *
from dateutil.parser import *
from VipType import *

class DateUtil():
	def isVipValid(self,time,vip_type):
		start_time = parse(time)
		end_time = start_time
		months_num = 1
		if vip_type == VipType.month.value:
			months_num = 1
		elif vip_type == VipType.quarter.value:
			months_num = 3
		elif vip_type == VipType.half_year.value:
			months_num = 6
		elif vip_type == VipType.year.value:
			months_num = 12
		elif vip_type == VipType.forever.value:
			return True
		else:
			return False
		end_time = start_time+relativedelta(months=+months_num)
		print(start_time,end_time)
		return (end_time > datetime.now())







