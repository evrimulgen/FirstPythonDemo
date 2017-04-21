#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import requests
from requests.utils import quote
from threading import Thread

s = requests.Session()
headers = {
	"user-agent": r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
# 去掉html标签，去掉指定名词
rule1 = re.compile('<[^>]+>|^[A-Za-z]+|正品|专营店|旗舰店|专卖店|特价')
page_size = 60
results = []
brand_list = []


# 通过 商品关键字 获取品牌列表
def get_brand_list(key_word):
	global headers
	key_word = key_word.strip()
	# 模拟浏览器 转换字符串str类型为url编码
	key_word = quote(key_word.encode("GBK"))
	url = r'https://list.tmall.com/ajax/allBrandShowForGaiBan.htm?q='
	url = "".join([url, key_word])
	json_list = s.get(url, headers=headers).json()
	# 格式化输入json串
	# print(json.dumps(json_list, indent=2))
	brand_list = []
	for item in json_list:
		brand_name = item['title']
		brand_name.strip().strip('/').strip()
		if '/' not in brand_name:
			brand_list.append(brand_name)
		else:
			for brand_ in brand_name.split('/'):
				brand_list.append(brand_.strip())
	return brand_list


def get_title_list_by_page_index(key_word, page_index):
	title_list = []
	global headers, rule1
	key_word = key_word.strip()
	url = r'https://s.taobao.com/list?json=on'
	url = "&".join([url, "q=" + key_word, "s=" + str(page_index * page_size)])
	json_list = s.get(url, headers=headers).json()
	if 'data' in json_list['mods']['itemlist']:
		auctions = json_list['mods']['itemlist']['data']['auctions']
		for auction in auctions:
			title = rule1.sub('', auction['title'])
			nick = rule1.sub('', auction['nick'])
			title = title.replace(nick, '')
			title_list.append(title)
	return title_list


def get_title_list_by_total_page(key_word, total_page):
	title_list = []
	total_page_count = 1
	if total_page is not None and total_page != '':
		total_page_count = int(total_page)
		if total_page_count < 1:
			total_page_count = 1
	thread_list = []
	for index in range(0, total_page_count):
		__thread = TitlesThread(target=get_title_list_by_page_index, args=(key_word, index + 1))
		__thread.start()
		thread_list.append(__thread)

	for thread_item in thread_list:
		title_list = title_list + thread_item.join()
	return title_list


# 获取 去 品牌名 的标题
def get_processed_title(brand_list, title_list):
	for index, value in enumerate(title_list):
		for val in brand_list:
			title_list[index] = title_list[index].replace('\\', '').replace('/', '').replace(val, '').strip()
	return title_list


class TitlesThread(Thread):
	def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
		Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
		self._result = None

	def run(self):
		if self._target is not None:
			self._result = self._target(*self._args, **self._kwargs)

	def join(self, timeout=None):
		Thread.join(self)
		return self._result