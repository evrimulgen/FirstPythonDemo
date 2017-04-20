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
		if vip_type == VipType.trial.value:
			end_time = start_time + relativedelta(days=+2)
		elif vip_type == VipType.month.value:
			end_time = start_time + relativedelta(months=+1)
		elif vip_type == VipType.half_year.value:
			end_time = start_time + relativedelta(months=+6)
		elif vip_type == VipType.year.value:
			end_time = start_time + relativedelta(months=+12)
		elif vip_type == VipType.forever.value:
			return True
		else:
			return False

		return (end_time > datetime.now())

	def getDateline(self,time,vip_type):
		start_time = parse(time)
		return str(self.__getDateline(start_time,vip_type))

	def __getDateline(self,time,vip_type):
		if vip_type == VipType.trial.value:
			return str(time + relativedelta(days=+2))
		if vip_type == VipType.month.value:
			return str(time + relativedelta(months=+1))
		elif vip_type == VipType.half_year.value:
			return str(time + relativedelta(months=+6))
		elif vip_type == VipType.year.value:
			return str(time + relativedelta(months=+12))
		elif vip_type == VipType.forever.value:
			return '永久'
		else:
			return '无效'







