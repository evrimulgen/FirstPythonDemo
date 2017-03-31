#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask,request,render_template,make_response,url_for,redirect
from UserUtil import *

import json
import SearchLogic

app = Flask(__name__)

######################## 客户端后台服务模块 ########################

# 判断登录是否有效
@app.route('/login', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
	elif request.method == 'GET':
		username = request.args.get('username')
		password = request.args.get('password')
	else:
		return json.dumps(())
	return json.dumps(check_user_info(username,password,False))

# 搜索分裂标题
@app.route('/search', methods=['POST','GET'])
def search():
	username = ''
	password = ''
	key_word = ''
	number = 1
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		key_word = request.form['keyword']
		number = request.form['pagesize']
	elif request.method == 'GET':
		username = request.args.get('username')
		password = request.args.get('password')
		key_word = request.args.get('keyword')
		number = request.args.get('pagesize')
	else:
		return json.dumps(())
	result = check_user_info(username,password,True)
	if result['status'] == False:
		return json.dumps(result)
	brand_list = SearchLogic.get_brand_list(key_word)
	results = SearchLogic.get_processed_title(brand_list,SearchLogic.get_title_list_by_total_page(key_word,number))
	result['list'] = results
	return json.dumps(result)

# 超级管理员
@app.route('/adminlogin', methods=['POST','GET'])
def adminLogin():
	error = ''
	username = ''
	password = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username != 'admin' or password != '111111':
			error= "用户名或密码错误"
		else:
			user_infos_temp = get_all_user_info()
			user_infos = list()
			for user_info_temp in user_infos_temp:
				item = list()
				for index,value in enumerate(user_info_temp):
					if index == 6:
						item.append(get_vip_type_desc_by_value(value))
					else:
						item.append(value)
				user_infos.append(item)
			resp = make_response(render_template('manager.html',user_infos=user_infos))
			resp.set_cookie('username',username)
			return resp
			# return redirect(url_for('adminManager',username=username,password=password))
		# return render_template('manager.html',results = results,brand_key_word = brand_key,title_key_word = title_key,divide_num = divide_num,brand_name_list = brand_list,brand_name_list_exp=brand_name_list_exp)
	return render_template('login.html',username = username,password = password,error = error)


# 添加用户
@app.route('/admin_add', methods=['POST'])
def adminAdd():
	result = request.get_json()
	rows = add_new_user(result["user_name"],result["phone_number"],result["vip_type"])	
	if rows == 1:
		# 待优化 取最后一条数据
		user_infos_temp = get_all_user_info()
		user_infos = list()
		for user_info_temp in user_infos_temp:
			item = list()
			for index,value in enumerate(user_info_temp):
				if index == 6:
					item.append(get_vip_type_desc_by_value(value))
				else:
					item.append(value)
			user_infos.append(item)
		result = get_ok_msg()
		result['list'] = user_infos[0:1][0]
		# resp = make_response(render_template('manager.html',user_infos=user_infos))
		# return resp
		return json.dumps(result)
	else:
		return json.dumps(get_err_msg(6))



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0') 

