#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask, request, render_template, make_response
from flask_compress import Compress

import SearchLogic
from UserUtil import *

compress = Compress()


def create_app():
	app = Flask(__name__)
	compress.init_app(app)
	return app


app = create_app()


######################## 客户端后台服务模块 ########################

# 判断登录是否有效
@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
	elif request.method == 'GET':
		username = request.args.get('username')
		password = request.args.get('password')
	else:
		return json.dumps(())
	return json.dumps(check_user_info(username, password, False))


# 搜索分裂标题
@app.route('/search', methods=['POST', 'GET'])
def search():
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
	result = check_user_info(username, password, True)
	if result['status'] == False:
		return json.dumps(result)
	if key_word is None or key_word == '':
		return json.dumps(())
	results = SearchLogic.get_processed_title(key_word, number)
	result['list'] = results
	return json.dumps(result)


######################## 管理员后台服务模块 ########################

# 超级管理员
@app.route('/adminlogin', methods=['POST', 'GET'])
def adminLogin():
	error = ''
	username = ''
	password = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username != 'admin' or password != '.111admin111.':
			error = "用户名或密码错误"
		else:
			user_infos = get_all_user_info()
			resp = make_response(render_template('manager.html', user_infos=user_infos))
			# resp.set_cookie('username',username)
			return resp
		# return redirect(url_for('adminManager',username=username,password=password))
		# return render_template('manager.html',results = results,brand_key_word = brand_key,title_key_word = title_key,divide_num = divide_num,brand_name_list = brand_list,brand_name_list_exp=brand_name_list_exp)
	return render_template('login.html', username=username, password=password, error=error)


# 添加用户
@app.route('/admin_add', methods=['POST'])
def adminAdd():
	result = request.get_json()
	try:
		rows = add_new_user(result["account"], result["user_name"], result["vip_type"])
		if rows == 1:
			# 待优化 取最后一条数据
			result = get_ok_msg()
			result['list'] = get_last_user_info()
			return json.dumps(result)
	except sqlite3.Error as e:
		print(str(e))
		print('traceback.print_exc():', traceback.print_exc())
	return json.dumps(get_err_msg(6))


# 修改用户信息
@app.route('/admin_update', methods=['POST'])
def adminUpdate():
	result = request.get_json()
	try:
		rows = update_one_user(result["account"], result["user_name"], result["blance_times"], result["vip_type"])
		if rows == 1:
			result = get_ok_msg()
			return json.dumps(result)
	except sqlite3.Error as e:
		print(str(e))
		print('traceback.print_exc():', traceback.print_exc())
	return json.dumps(get_err_msg(6))


# 删除用户
@app.route('/admin_delete', methods=['POST'])
def adminDelete():
	try:
		result = request.get_json()
		rows = delete_one_user(result["account"])
		if rows == 1:
			result = get_ok_msg()
			return json.dumps(result)
	except sqlite3.Error as e:
		print(str(e))
		print('traceback.print_exc():', traceback.print_exc())
	return json.dumps(get_err_msg(6))


if __name__ == '__main__':
	# app.debug = True
	# app.run(host='0.0.0.0')
	app.run()
