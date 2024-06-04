from flask import Flask, render_template, request, redirect, session, jsonify, send_file, render_template_string
from flask import Blueprint
import sqlite3
from flask import Blueprint

login_register_bp= Blueprint("login_register", __name__)


# 注册用户
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


def register_admin(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE admins SET password = ? WHERE manageID = ?", (password, username))
    conn.commit()
    conn.close()


def register_farmer(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO farmers (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


# 验证登录
def login_user(username, password, user_type):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    if user_type == "0":
        c.execute("SELECT password FROM admins WHERE manageID=?", (username,))
    elif user_type == "1":
        c.execute("SELECT password FROM farmers WHERE username=?", (username,))
    elif user_type == "2":
        c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == password:
        return 0
    return None


# 注册页面
@login_register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_type = request.form['register_type']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        if register_type == "0":
            c.execute("SELECT manageID,password FROM admins WHERE manageID=?", (username,))
            result = c.fetchone()

            if result is None:
                conn.close()
                return "无管理权限"
            elif result[1] is not None:  # password不为空
                print("test")
                conn.close()
                return "该权限ID已注册"
        elif register_type == "1":
            c.execute("SELECT username FROM farmers WHERE username=?", (username,))
        elif register_type == "2":
            c.execute("SELECT username FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()
        if result:
            return "该用户名已被注册，请选择其他用户名。"

        if register_type == "0":
            register_admin(username, password)
        elif register_type == "1":
            register_farmer(username, password)
        elif register_type == "2":
            register_user(username, password)
        return redirect('/login')
    return render_template('register.html')


# 登录页面
@login_register_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        res = login_user(username, password, user_type)
        if res is not None:
            session['username'] = username
            session['user_type'] = user_type
            if user_type == "0":
                return redirect('/admin')
            elif user_type == "1":
                return redirect('/famer')
            elif user_type == "2":
                return redirect('/user')
        else:
            return "登录失败，请检查用户名和密码。"
    return render_template('login.html')


# 用户注销
@login_register_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect('/')
