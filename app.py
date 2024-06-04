#from flask import Flask, render_template, request, redirect, session,jsonify,send_file,render_template_string
#from flask import Flask, url_for,jsonify
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

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 设置用于会话加密的密钥

#socketio = SocketIO(app)

# 创建数据库连接和表
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, is_admin INTEGER)''')
    conn.commit()
    conn.close()


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


# 注册页面
@app.route('/register', methods=['GET', 'POST'])
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
    return render_template('register_haha.html')


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
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
    return render_template('login_haha.html')


# 用户注销
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect('/')


# 用户页面
@app.route('/user')
def user():
    if 'username' in session and session['user_type'] == "2":
        return render_template('user.html')
    else:
        return redirect('/login')


# ---------------------------------------
# underwater 页面
@app.route('/underwater')
def underwater():
    if 'username' in session:
        # 读取Excel文件
        df = pd.read_excel('data.xlsx')
        # 获取第一列所有不同的数据
        col1_options = df.iloc[:, 0].unique()
        # 获取第一行的标题，去掉第一列的标题
        header_options = df.columns[1:].tolist()
        # 渲染模板并传递unique_values
        # 读取.xlsx文件

        dff = pd.read_excel('data.xlsx', header=0)
        # 获取最后一行数据
        data = dff.iloc[-1]

        dff = pd.DataFrame(data)

        # 将DataFrame转换为HTML表格
        html_table = dff.to_html(index=True, header=False)

        return render_template('underwater.html', col1_options=col1_options, header_options=header_options,
                               table=html_table)






    else:
        return redirect('/login')


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
# underwater 页面
@app.route('/underwater_plus')
def underwater_plus():
    if 'username' in session:
        # 读取Excel文件
        df = pd.read_excel('data.xlsx')
        # 获取第一列所有不同的数据
        col1_options = df.iloc[:, 0].unique()
        # 获取第一行的标题，去掉第一列的标题
        header_options = df.columns[1:].tolist()
        # 渲染模板并传递unique_values
        # 读取.xlsx文件

        dff = pd.read_excel('data.xlsx', header=0)
        # 获取最后一行数据
        data = dff.iloc[-1]

        dff = pd.DataFrame(data)

        # 将DataFrame转换为HTML表格
        html_table = dff.to_html(index=True, header=False)


        return render_template('underwater_plus.html', col1_options=col1_options, header_options=header_options,table=html_table)


    else:
        return redirect('/login')


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


# ---------------------------------------
# ---------------------------------------
# underwater 页面
@app.route('/underwater__famer')
def underwater_famer():
    if 'username' in session:
        # 读取Excel文件
        df = pd.read_excel('data.xlsx')
        # 获取第一列所有不同的数据
        col1_options = df.iloc[:, 0].unique()
        # 获取第一行的标题，去掉第一列的标题
        header_options = df.columns[1:].tolist()
        # 渲染模板并传递unique_values
        # 读取.xlsx文件

        dff = pd.read_excel('data.xlsx', header=0)
        # 获取最后一行数据
        data = dff.iloc[-1]

        dff = pd.DataFrame(data)

        # 将DataFrame转换为HTML表格
        html_table = dff.to_html(index=True, header=False)

        return render_template('underwater__famer.html', col1_options=col1_options, header_options=header_options,
                               table=html_table)




    else:
        return redirect('/login')


@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # 读取Excel文件
    df = pd.read_excel('data.xlsx')
    selected_col1_value = request.form.get('col1_select')
    selected_header = request.form.get('header_select')

    # 根据用户选择过滤数据
    filtered_df = df[(df.iloc[:, 0] == selected_col1_value)]

    # 创建图表
    plt.figure()
    filtered_df[selected_header].plot(kind='bar')  # 假设我们使用条形图
    plt.title(f'Data for {selected_col1_value}')
    plt.xlabel(selected_header)

    # 将图表保存到内存中的IO对象
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # 清空图表
    plt.close()

    # 返回图表的PNG数据
    #return send_file(buf, mimetype='image/png')
    return render_template('indexx.html')


@app.route('/your-flask-route', methods=['POST'])
def handle_form_data():
    # 获取表单数据
    col1_value = request.form['col1_select']
    header_value = request.form['header_select']
    df = pd.read_excel('data.xlsx')
    columns = df.columns
    column_index = columns.get_loc(header_value)


    # 根据用户选择过滤数据
    filtered_df = df[(df.iloc[:, 0] == col1_value)]
    x = filtered_df.iloc[:, [0]]
    y=filtered_df.iloc[:, [column_index]]


    # 创建图表
    #print(selected_columns_df)
    x_data = x.values.tolist()
    y_data = y.values.tolist()

    # 打印二维列表
    #print(data_without_index_header)
    # 现在你可以使用这些值进行进一步的处理
    print(f"Selected Column 1 Value: {col1_value}")
    print(f"Selected Header Value: {header_value}")
    length = len(x_data)
    x_data = list(range(1, len(x_data) + 1))

    # 返回响应
    #return render_template('indexx.html')
    return render_template_string('''
           <!DOCTYPE html>
           <html>
           <head>
               <title>Scatter Plot from NumPy Array</title>
               <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
           </head>
           <body>
               <canvas id="scatterChart"></canvas>
               <script>
                   var xData = {{ x_data | safe }};
                   var yData = {{ y_data | safe }};
                   var dataLength = {{ length }};
                   var ctx = document.getElementById('scatterChart').getContext('2d');
                   var scatterChart = new Chart(ctx, {
                       type: 'scatter',
                       data: {
                           datasets: [{
                               label: 'My Scatter Data',
                               data: xData.map((x, i) => ({x: x, y: yData[i]})).slice(0, dataLength),
                               backgroundColor: 'rgba(0, 123, 255, 0.5)',
                               borderColor: 'rgba(0, 123, 255, 1)',
                               borderWidth: 1
                           }]
                       },
                       options: {
                           scales: {
                               x: {
                                   title: {
                                       display: true,
                                       text: 'X Axis'
                                   }
                               },
                               y: {
                                   title: {
                                       display: true,
                                       text: 'Y Axis'
                                   }
                               }
                           }
                       }
                   });
               </script>
           </body>
           </html>
       ''', x_data=x_data, y_data=y_data, length=length)


# datacenter 页面
@app.route('/datacenter__famer')
def datacenter_famer():
    if 'username' in session:
        return render_template('datacenter_famer.html')
    else:
        return redirect('/login')





#----------------------------智能中心功能实现----------------------------
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

# intelligentcenter 页面
@app.route('/intelligentcenter_plus', methods=['GET', 'POST'])
def intelligentcenter_plus():
    if 'username' in session:
        #获取传感器数据
        try:
            temperature1, wind_direction1, wind_speed1, humidity1, air_quality1 = get_weather_data()
        except Exception as e:
            return f"Error getting weather data: {e}", 500

        # 读取 Excel 文件中的水温、pH 值和浊度数据
        try:
             water_temperature,ph,turbidity=get_water_quality_data()

             '''
            df = pd.read_excel('水质数据.xlsx', usecols=['水温（℃）', 'pH(无量纲)', '浊度（NTU）'])
            latest_row = df.iloc[-1]
            '''

        except Exception as e:
            return f"Error reading water quality data: {e}", 500
        
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

        return render_template('intelligentcenter_plus.html', water_temperature=water_temperature, ph=ph, turbidity=turbidity,
                               alarm_message=alarm_message, water_temperature_threshold=water_temperature_threshold,
                               ph_threshold=ph_threshold, turbidity_threshold=turbidity_threshold,temperature=temperature1,
                               wind_direction=wind_direction1,
                               wind_speed=wind_speed1,
                               humidity=humidity1,
                               air_quality=air_quality1)
    else:
        return redirect('/login')

@app.route('/intelligentcenter')
def intelligentcenter():
    if 'username' in session:
        temperature1, wind_direction1, wind_speed1, humidity1, air_quality1 = get_weather_data()
        return render_template('intelligentcenter.html',temperature=temperature1,
                               wind_direction=wind_direction1,
                               wind_speed=wind_speed1,
                               humidity=humidity1,
                               air_quality=air_quality1)
    else:
        return redirect('/login')


# intelligentcenter 页面
@app.route('/intelligentcent_famer')
def intelligentcent_famer():
    if 'username' in session:
        return render_template('intelligentcent_famer.html')
    else:
        return redirect('/login')

# upup 页面
@app.route('/upup')
def upup():
    if 'username' in session:
        return render_template('upup.html')
    else:
        return redirect('underwater_plus')


 



if __name__ == '__main__':
    create_database()
    app.run(debug=True)
    #socketio.run(app)
  


#------------------------------智能中心功能实现到此结束-----------------------------
