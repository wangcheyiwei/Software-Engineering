import base64
import sqlite3

from flask import Flask, render_template, request, redirect, session, jsonify, send_file, render_template_string
import pandas as pd
from flask import Blueprint
from matplotlib import pyplot as plt
from io import BytesIO
from module_code import select_code

underwater_bp = Blueprint("underwater", __name__)


# underwater 页面
@underwater_bp.route('/underwater_plus', methods=['GET', 'POST'])
def underwater_plus():
    # ----------------上传鱼类信息部分--------------------------------
    if request.method == 'POST':
        if 'fish_submit_button' in request.form:
            # 处理鱼群信息表单提交
            upload_date = request.form['upload_date']
            fish_species = request.form['species_select']
            weight = request.form['weight']
            length1 = request.form['length1']
            length2 = request.form['length2']
            length3 = request.form['length3']
            height = request.form['height']
            width = request.form['width']
            num = int(request.form['num'])

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            for _ in range(num):
                cursor.execute(
                    'INSERT INTO fish (Species,Weight,Length1,Length2,Length3,Height,Width) VALUES (?, ?,?,?,?,?,?)',
                    (fish_species, weight, length1, length2, length3, height, width))
            conn.commit()
            conn.close()

    if 'username' in session:
        # ------------------水质信息表格部分-----------------------
        # 读取Excel文件，获取时间选项和物质选项
        df = pd.read_excel('处理后的数据/data.xlsx')
        col1_options = df.iloc[:, 0].unique()
        header_options = df.columns[1:].tolist()

        # 读取.xlsx文件，获取最新数据
        dff = pd.read_excel('处理后的数据/data.xlsx', header=0)
        data = dff.iloc[-1]  # 最后一行数据
        dff = pd.DataFrame(data)
        # 将DataFrame转换为HTML表格
        html_table = dff.to_html(index=True, header=False)

        # -----------------鱼类信息部分------------------------------
        # 读取鱼类信息
        fish_weight = []
        fish_size = []
        select_code1 = "SELECT species,COUNT(*) FROM fish GROUP BY species"
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(select_code1)
        species_num = c.fetchall()  # 鱼群种类环状图

        for i in range(7):  # 鱼群重量图
            c.execute(select_code.codes[i])
            fish_weight.append(c.fetchall())

        for i in range(7):  # 鱼群尺寸图
            c.execute(select_code.size_codes[i])
            fish_size.append(c.fetchall())
        conn.close()

        return render_template('underwater_plus.html',
                               col1_options=col1_options, header_options=header_options, table=html_table,
                               species_num=species_num,
                               fish_weight=fish_weight, fish_size=fish_size)
    else:
        return redirect('/login')


@underwater_bp.route('/underwater__famer', methods=['GET', 'POST'])
def underwater__famer():
    if request.method == 'POST':
        if 'fish_submit_button' in request.form:
            # 处理鱼群信息表单提交
            upload_date = request.form['upload_date']
            fish_species = request.form['species_select']
            weight = request.form['weight']
            length1 = request.form['length1']
            length2 = request.form['length2']
            length3 = request.form['length3']
            height = request.form['height']
            width = request.form['width']
            num = int(request.form['num'])

            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            for _ in range(num):
                cursor.execute(
                    'INSERT INTO fish (Species,Weight,Length1,Length2,Length3,Height,Width) VALUES (?, ?,?,?,?,?,?)',
                    (fish_species, weight, length1, length2, length3, height, width))
            conn.commit()
            conn.close()

    if 'username' in session:
        df = pd.read_excel('处理后的数据/data.xlsx')
        col1_options = df.iloc[:, 0].unique()
        # 获取第一行的标题，去掉第一列的标题
        header_options = df.columns[1:].tolist()
        # 渲染模板并传递unique_values
        # 读取.xlsx文件
        dff = pd.read_excel('处理后的数据/data.xlsx', header=0)
        # 获取最后一行数据
        data = dff.iloc[-1]

        dff = pd.DataFrame(data)

        # 将DataFrame转换为HTML表格
        html_table = dff.to_html(index=True, header=False)

        # 读取鱼类信息
        fish_weight = []
        fish_size = []
        select_code1 = "SELECT species,COUNT(*) FROM fish GROUP BY species"  # 鱼种类
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(select_code1)
        species_num = c.fetchall()  # 鱼群种类环状图

        for i in range(7):
            c.execute(select_code.codes[i])
            fish_weight.append(c.fetchall())
        print(fish_weight)

        for i in range(7):
            c.execute(select_code.size_codes[i])
            fish_size.append(c.fetchall())
        conn.close()
        print(fish_size)
        return render_template('underwater__famer.html',
                               col1_options=col1_options, header_options=header_options, table=html_table,
                               species_num=species_num,
                               fish_weight=fish_weight, fish_size=fish_size)
    else:
        return redirect('/login')


@underwater_bp.route('/underwater')
def underwater():
    if 'username' in session:
        df = pd.read_excel('处理后的数据/data.xlsx')
        col1_options = df.iloc[:, 0].unique()
        header_options = df.columns[1:].tolist()
        dff = pd.read_excel('处理后的数据/data.xlsx', header=0)
        data = dff.iloc[-1]
        dff = pd.DataFrame(data)
        html_table = dff.to_html(index=True, header=False)

        # 读取鱼类信息
        fish_weight = []
        fish_size = []
        select_code1 = "SELECT species,COUNT(*) FROM fish GROUP BY species"
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(select_code1)
        species_num = c.fetchall()  # 鱼群种类环状图

        for i in range(7):  # 鱼群重量图
            c.execute(select_code.codes[i])
            fish_weight.append(c.fetchall())
        for i in range(7):  # 鱼群尺寸图
            c.execute(select_code.size_codes[i])
            fish_size.append(c.fetchall())
        conn.close()
        return render_template('underwater.html',
                               col1_options=col1_options, header_options=header_options, table=html_table,
                               species_num=species_num,
                               fish_weight=fish_weight, fish_size=fish_size)
    else:
        return redirect('/login')


@underwater_bp.route('/upup')
def upup():
    if 'username' in session:
        return render_template('upup.html')
    else:
        return redirect('underwater_plus')


# 生成水质图表
@underwater_bp.route('/generate_water_chart', methods=['POST'])
def handle_form_data():
    # 获取表单数据
    col1_value = request.form['col1_select']
    header_value = request.form['header_select']
    print(f"Selected Column 1 Value: {col1_value}")
    print(f"Selected Header Value: {header_value}")

    df = pd.read_excel('处理后的数据/data.xlsx')
    columns = df.columns  # 所有列名称
    column_index = columns.get_loc(header_value)  # 选中的列索引

    # 根据用户选择过滤数据
    filtered_df = df[(df.iloc[:, 0] == col1_value)]  # 选中日期内的所有行
    x = filtered_df.iloc[:, [0]]  # 选中日期内的所有行中的第一列数值
    y = filtered_df.iloc[:, [column_index]]
    x_data = x.values.tolist()
    y_data = y.values.tolist()
    ydata = [item for sublist in y_data if sublist for item in sublist]

    # 现在你可以使用这些值进行进一步的处理

    length = len(x_data)
    x_data = list(range(1, len(x_data) + 1))
    print(x_data)
    print(ydata)

    # 返回响应
    return render_template("generate_water_chart.html", x_data=x_data, y_data=ydata, length=length)


# 在py文件中生成图表，将生成的图表传递给html文件（这里没用上）
@underwater_bp.route('/generate_chart', methods=['POST'])
def generate_chart():
    # 读取Excel文件
    df = pd.read_excel('处理后的数据/data.xlsx')
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

    # 将图表转换为Base64编码的字符串
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # 返回图表的Base64编码字符串到HTML模板
    return render_template('generate_chart.html', image_base64=image_base64)
