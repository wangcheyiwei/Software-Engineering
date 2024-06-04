from flask import Flask, render_template, request, redirect, session, jsonify, send_file, render_template_string
from flask import Flask, url_for, jsonify
#from flask_socketio import SocketIO, emit
from flask import render_template
import sqlite3
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import io
import threading
import time
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg

import base64

import os
import pandas as pd
from module_code import login_register_logout, underwater

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 设置用于会话加密的密钥

#socketio = SocketIO(app)
app.register_blueprint(underwater.underwater_bp)
app.register_blueprint(login_register_logout.login_register_bp)


# 创建数据库连接和表
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, is_admin INTEGER)''')
    conn.commit()
    conn.close()


# 设置用户为管理员
def set_user_as_admin(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET is_admin=1 WHERE username=?", (username,))
    conn.commit()
    conn.close()


# 项目介绍页面
@app.route('/')
def index():
    return render_template('index.html')


# 用户页面
@app.route('/user')
def user():
    if 'username' in session and session['user_type'] == "2":
        return render_template('user.html')
    else:
        return redirect('/login')


# -------------------------------------------
# datacenter 页面
@app.route('/datacenter')
def datacenter():
    if 'username' in session:
        return render_template('datacenter.html')
    else:
        return redirect('/login')


# ---------------------------------------
# 管理员页面
@app.route('/admin')
def admin():
    if 'username' in session and session['user_type'] == "0":
        return render_template('admin.html')
    else:
        return redirect('/login')


# 添加用户
@app.route('/edit_user_info/add', methods=['POST'])
def add_user():
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('users.db')
    # 创建一个游标对象
    cursor = conn.cursor()

    # 获取表单数据
    username = request.form['username']
    password = request.form['password']
    # 插入新用户数据到数据库
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    # 关闭数据库连接
    conn.close()

    # 重定向到编辑用户信息页面
    return redirect(url_for('edit_user_info'))


# 修改用户信息页面
@app.route('/edit_user_info/edit/<string:username>', methods=['GET', 'POST'])
def edit_user(username):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('users.db')
    # 创建一个游标对象
    cursor = conn.cursor()

    # 如果是 POST 请求，表示用户提交了修改后的信息
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        # 更新数据库中的用户信息
        cursor.execute('UPDATE users SET username = ?, password = ? WHERE username = ?',
                       (new_username, new_password, username))
        conn.commit()
        # 关闭数据库连接
        conn.close()

        # 重定向到编辑用户信息页面
        return redirect(url_for('edit_user_info'))

    # 如果是 GET 请求，显示编辑用户信息页面
    else:
        # 查询用户当前信息
        cursor.execute('SELECT username, password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        # 关闭数据库连接
        conn.close()

        return render_template('edit_user.html', user=user, username=username)


# 更新用户信息
@app.route('/edit_user_info/update/<string:username>', methods=['POST'])
def update_user(username):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('users.db')
    # 创建一个游标对象
    cursor = conn.cursor()

    # 获取表单数据
    new_username = request.form['username']
    password = request.form['password']
    # 更新用户信息
    cursor.execute('UPDATE users SET username = ?, password = ? WHERE username = ?', (new_username, password, username))
    conn.commit()
    # 关闭数据库连接
    conn.close()

    # 重定向到编辑用户信息页面
    return redirect(url_for('edit_user_info'))


# 删除用户
@app.route('/edit_user_info/delete/<string:username>')
def delete_user(username):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('users.db')
    # 创建一个游标对象
    cursor = conn.cursor()

    # 删除指定用户
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    # 关闭数据库连接
    conn.close()

    # 重定向到编辑用户信息页面
    return redirect(url_for('edit_user_info'))


# 编辑用户信息页面
@app.route('/edit_user_info')
def edit_user_info():
    # 连接到 SQLite 数据库
    conn = sqlite3.connect('users.db')
    # 创建一个游标对象
    cursor = conn.cursor()

    # 执行查询语句，获取所有用户信息
    cursor.execute('SELECT* FROM users')
    # 获取查询结果
    users = cursor.fetchall()
    # 关闭数据库连接
    conn.close()

    # 渲染 HTML 页面并传递用户信息
    return render_template('edit_user_info.html', users=users)


# ---------------------------------------
# ---------------------------------------


# datacenter 页面
@app.route('/datacenter_plus')
def datacenter_plus():
    if 'username' in session:
        return render_template('datacenter_plus.html')
    else:
        return redirect('/login')


# intelligentcenter 页面

# ---------------------------------------

# 设置用户为管理员
@app.route('/admin/set_admin/<username>')
def set_admin(username):
    if 'username' in session and session['user_type'] == "0":
        set_user_as_admin(username)
        return f"已将用户 '{username}' 设置为管理员。"
    else:
        return redirect('/login')


# 养殖户页面
@app.route('/famer')
def famer():
    if 'username' in session and session['user_type'] == "1":
        return render_template('famer.html')
    else:
        return redirect('/login')


# datacenter 页面
@app.route('/datacenter__famer')
def datacenter_famer():
    if 'username' in session:
        return render_template('datacenter_famer.html')
    else:
        return redirect('/login')


# ----------------------------智能中心功能实现----------------------------
# 全局变量,用于存储最新的水质数据和气象数据
latest_water_quality_data = None
latest_weather_data = None


# 定期读取水质数据 Excel 文件并更新全局变量的函数
def update_water_quality_data():
    global latest_water_quality_data
    while True:
        try:
            excel_file = '水质数据.xlsx'
            if os.path.exists(excel_file):
                df = pd.read_excel('水质数据.xlsx', usecols=['水温（℃）', 'pH(无量纲)', '浊度（NTU）'])
                if df.empty:
                    raise Exception("水质数据文件中没有数据！")

                latest_row = df.iloc[-1]
                water_temperature = latest_row['水温（℃）']
                ph = latest_row['pH(无量纲)']
                turbidity = latest_row['浊度（NTU）']

                latest_water_quality_data = (water_temperature, ph, turbidity)
            else:
                raise Exception("水质数据文件不存在！")
        except Exception as e:
            print(f"Error getting water quality data: {e}")
        time.sleep(60)  # 每60秒读取一次数据


# 定期读取气象数据 Excel 文件并更新全局变量的函数
def update_weather_data():
    global latest_weather_data
    while True:
        try:
            excel_file = './weather_data.xlsx'
            if os.path.exists(excel_file):
                df = pd.read_excel(excel_file)
                if df.empty:
                    raise Exception("气象数据文件中没有数据！")
                temperature = df['气温'].iloc[-1]
                wind_direction = df['风向'].iloc[-1]
                wind_speed = df['风速'].iloc[-1]
                humidity = df['湿度'].iloc[-1]
                air_quality = df['空气质量'].iloc[-1]
                latest_weather_data = (temperature, wind_direction, wind_speed, humidity, air_quality)
            else:
                raise Exception("气象数据文件不存在！")
        except Exception as e:
            print(f"Error getting weather data: {e}")
        time.sleep(60)  # 每60秒读取一次数据


# 启动定期读取数据的线程
water_quality_update_thread = threading.Thread(target=update_water_quality_data)
water_quality_update_thread.daemon = True
water_quality_update_thread.start()

weather_update_thread = threading.Thread(target=update_weather_data)
weather_update_thread.daemon = True
weather_update_thread.start()


def get_water_quality_data():
    global latest_water_quality_data
    if latest_water_quality_data is not None:
        return latest_water_quality_data
    else:
        raise Exception("Water quality data not available")


def get_weather_data():
    global latest_weather_data
    if latest_weather_data is not None:
        return latest_weather_data
    else:
        raise Exception("Weather data not available")


'''
def get_weather_data():
    excel_file = './weather_data.xlsx'
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        if df.empty:
            raise Exception("文件中没有数据！")
        temperature = df['气温'].iloc[-1]
        wind_direction = df['风向'].iloc[-1]
        wind_speed = df['风速'].iloc[-1]
        humidity = df['湿度'].iloc[-1]
        air_quality = df['空气质量'].iloc[-1]
        return temperature, wind_direction, wind_speed, humidity, air_quality
    else:
        raise Exception("文件不存在！")
'''
def get_water_quality_data1():
    # 读取 Excel 文件中的必要参数
    df = pd.read_excel('水质数据.xlsx')
    latest_row = df.iloc[-1]
    water_temperature = latest_row['水温（℃）']
    ph = latest_row['pH(无量纲)']
    dissolved_oxygen = latest_row['溶氧量(mg/L)']
    permanganate_index = latest_row['高锰酸盐指数（mg/L）']
    ammonia_nitrogen = latest_row['氨氮（mg/L）']
    total_phosphorus = latest_row['总磷（mg/L）']
    total_nitrogen = latest_row['总氮（mg/L）']
    return water_temperature, ph, dissolved_oxygen, permanganate_index, ammonia_nitrogen, total_phosphorus, total_nitrogen

# 环境质量标准
quality_standards = {
    "水温（℃）": [None, None, None, None, None],  # 需特殊处理
    "pH(无量纲)": [9, 9, 9, 9, 9],
    "溶氧量(mg/L)": [7.5, 6, 5, 3, 2],
    "高锰酸盐指数（mg/L）": [2, 4, 6, 10, 15],
    "氨氮（mg/L）": [0.15, 0.5, 1.0, 1.5, 2.0],
    "总磷（mg/L）": [0.02, 0.1, 0.2, 0.3, 0.4],
    "总氮（mg/L）": [0.2, 0.5, 1.0, 1.5, 2.0],
    
}

def calculate_score(row):
    score = 0
    for parameter, thresholds in quality_standards.items():
        value = row.get(parameter)
        if value is None:
            continue
        if parameter == "水温（℃）":
            # 水温特殊处理
        
            score += 3
        elif parameter == "溶氧量(mg/L)":
            if float(value) >= thresholds[0]:
                score += 5
            elif float(value) >= thresholds[1]:
                score += 4
            elif float(value) >= thresholds[2]:
                score += 3
            elif float(value) >= thresholds[3]:
                score += 2
            elif float(value) >= thresholds[4]:
                score += 1
            else:
                score += 0
            
        elif parameter == "pH(无量纲)":
            if float(value)>=6 and value<=9:
                score += 5
            else:
                score+=-1



        else:
            # 其他参数按照标准处理
            if float(value) <= thresholds[0]:
                score += 5
            elif float(value) <= thresholds[1]:
                score += 4
            elif float(value) <= thresholds[2]:
                score += 3
            elif float(value) <= thresholds[3]:
                score += 2
            elif float(value) <= thresholds[4]:
                score += 1
            else:
                score += 0
    return score

# intelligentcenter 页面
@app.route('/intelligentcenter_plus', methods=['GET', 'POST'])
def intelligentcenter_plus():
    if 'username' in session:
        # 获取传感器数据
        try:
            temperature1, wind_direction1, wind_speed1, humidity1, air_quality1 = get_weather_data()
        except Exception as e:
            return f"Error getting weather data: {e}", 500

        try:
            water_temperature1, ph1, dissolved_oxygen, permanganate_index, ammonia_nitrogen, total_phosphorus, total_nitrogen = get_water_quality_data1()
        except Exception as e:
            return f"Error reading water quality data: {e}", 500
        

        # 读取 Excel 文件中的水温、pH 值和浊度数据
        try:
             water_temperature,ph,turbidity=get_water_quality_data()
        except Exception as e:
            return f"Error reading water quality data: {e}", 500
        
             
       
        row_data = {
            "水温（℃）": water_temperature1,
            "pH(无量纲)": ph1,
            "溶氧量(mg/L)": dissolved_oxygen,
            "高锰酸盐指数（mg/L）": permanganate_index,
            "氨氮（mg/L）": ammonia_nitrogen,
            "总磷（mg/L）": total_phosphorus,
            "总氮（mg/L）": total_nitrogen
        }
        
        # 计算得分
        score = calculate_score(row_data)

        '''
        water_temperature = latest_row['水温（℃）']
        ph = latest_row['pH(无量纲)']
        turbidity = latest_row['浊度（NTU）']

        '''

        # 从session中获取用户设置的阈值,如果不存在则设置默认值
        water_temperature_threshold = session.get('water_temperature_threshold', 25.0)
        ph_threshold = session.get('ph_threshold', 7.5)
        turbidity_threshold = session.get('turbidity_threshold', 5.0)

        if request.method == 'POST':
            # 保存用户设置的新阈值到session
            water_temperature_threshold = float(request.form['water_temperature_threshold'])
            session['water_temperature_threshold'] = water_temperature_threshold
            ph_threshold = float(request.form['ph_threshold'])
            session['ph_threshold'] = ph_threshold
            turbidity_threshold = float(request.form['turbidity_threshold'])
            session['turbidity_threshold'] = turbidity_threshold

        alarm_message = ''

        if water_temperature > water_temperature_threshold or ph > ph_threshold or turbidity > turbidity_threshold:
            alarm_message = '警告:部分环境指标超出安全范围!'

        return render_template('intelligentcenter_plus.html', water_temperature=water_temperature, ph=ph,
                               turbidity=turbidity,
                               alarm_message=alarm_message, water_temperature_threshold=water_temperature_threshold,
                               ph_threshold=ph_threshold, turbidity_threshold=turbidity_threshold,
                               temperature=temperature1,
                               wind_direction=wind_direction1,
                               wind_speed=wind_speed1,
                               humidity=humidity1,
                               air_quality=air_quality1,score=score)
    else:
        return redirect('/login')


@app.route('/intelligentcenter')
def intelligentcenter():
    if 'username' in session:
        try:
            water_temperature1, ph1, dissolved_oxygen, permanganate_index, ammonia_nitrogen, total_phosphorus, total_nitrogen = get_water_quality_data1()
        except Exception as e:
            return f"Error reading water quality data: {e}", 500

        row_data = {
            "水温（℃）": water_temperature1,
            "pH(无量纲)": ph1,
            "溶氧量(mg/L)": dissolved_oxygen,
            "高锰酸盐指数（mg/L）": permanganate_index,
            "氨氮（mg/L）": ammonia_nitrogen,
            "总磷（mg/L）": total_phosphorus,
            "总氮（mg/L）": total_nitrogen
        }
        
        # 计算得分
        score = calculate_score(row_data)

        temperature1, wind_direction1, wind_speed1, humidity1, air_quality1 = get_weather_data()
        return render_template('intelligentcenter.html', temperature=temperature1,
                               wind_direction=wind_direction1,
                               wind_speed=wind_speed1,
                               humidity=humidity1,
                               air_quality=air_quality1,score=score)
    else:
        return redirect('/login')


# intelligentcenter 页面
@app.route('/intelligentcent_famer', methods=['GET', 'POST'])
def intelligentcent_famer():
    if 'username' in session:
        # 获取传感器数据
        try:
            temperature1, wind_direction1, wind_speed1, humidity1, air_quality1 = get_weather_data()
        except Exception as e:
            return f"Error getting weather data: {e}", 500

        # 读取 Excel 文件中的水温、pH 值和浊度数据
        try:
            water_temperature, ph, turbidity = get_water_quality_data()

            '''
            df = pd.read_excel('水质数据.xlsx', usecols=['水温（℃）', 'pH(无量纲)', '浊度（NTU）'])
            latest_row = df.iloc[-1]
            '''

        except Exception as e:
            return f"Error reading water quality data: {e}", 500

        try:
            water_temperature1, ph1, dissolved_oxygen, permanganate_index, ammonia_nitrogen, total_phosphorus, total_nitrogen = get_water_quality_data1()
        except Exception as e:
            return f"Error reading water quality data: {e}", 500

        row_data = {
            "水温（℃）": water_temperature1,
            "pH(无量纲)": ph1,
            "溶氧量(mg/L)": dissolved_oxygen,
            "高锰酸盐指数（mg/L）": permanganate_index,
            "氨氮（mg/L）": ammonia_nitrogen,
            "总磷（mg/L）": total_phosphorus,
            "总氮（mg/L）": total_nitrogen
        }
        
        # 计算得分
        score = calculate_score(row_data)


        '''
        water_temperature = latest_row['水温（℃）']
        ph = latest_row['pH(无量纲)']
        turbidity = latest_row['浊度（NTU）']

        '''

        # 从session中获取用户设置的阈值,如果不存在则设置默认值
        water_temperature_threshold = session.get('water_temperature_threshold', 25.0)
        ph_threshold = session.get('ph_threshold', 7.5)
        turbidity_threshold = session.get('turbidity_threshold', 5.0)

        if request.method == 'POST':
            # 保存用户设置的新阈值到session
            water_temperature_threshold = float(request.form['water_temperature_threshold'])
            session['water_temperature_threshold'] = water_temperature_threshold
            ph_threshold = float(request.form['ph_threshold'])
            session['ph_threshold'] = ph_threshold
            turbidity_threshold = float(request.form['turbidity_threshold'])
            session['turbidity_threshold'] = turbidity_threshold

        alarm_message = ''

        if water_temperature > water_temperature_threshold or ph > ph_threshold or turbidity > turbidity_threshold:
            alarm_message = '警告:部分环境指标超出安全范围!'

        return render_template('intelligentcent_famer.html', water_temperature=water_temperature, ph=ph,
                               turbidity=turbidity,
                               alarm_message=alarm_message, water_temperature_threshold=water_temperature_threshold,
                               ph_threshold=ph_threshold, turbidity_threshold=turbidity_threshold,
                               temperature=temperature1,
                               wind_direction=wind_direction1,
                               wind_speed=wind_speed1,
                               humidity=humidity1,
                               air_quality=air_quality1,score=score)
    else:
        return redirect('/login')


# ------------------------------智能中心功能实现到此结束-----------------------------


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
    # socketio.run(app)
