#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum,unique

@unique
class VipType(Enum):
	month = 0
	quarter = 1
	half_year = 2
	year = 3
	forever = 4
# 定义枚举类型
# https://taizilongxu.gitbooks.io/stackoverflow-about-python/content/7/README.html