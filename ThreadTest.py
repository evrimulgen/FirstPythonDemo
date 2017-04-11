#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time
from functools import wraps
import requests


exitFlag = 0

class MyThread(threading.Thread):
	def __init__(self,threadName):
		threading.Thread.__init__(self)
		self.threadName = threadName

	def run(self):
		request()

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
                ("request", str(t1-t0))
                )
        return result
    return function_timer

def request():
	url = r'http://127.0.0.1:5000/search?username=15010652066&password=ddd&keyword=%E7%AF%AE%E7%90%83&pagesize=5'
	result = requests.get(url)

@fn_timer
def test():
	print ("开始创建子线程")
	thread_list = []
	for i in range(100):
		thread_list.append(MyThread("Thread-" + str(i)))
	
	for thread in thread_list:
		thread.start()
	
	for thread in thread_list:
		thread.join()
	
	print ("退出主线程")

test()