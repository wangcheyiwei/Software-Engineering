from flask import Flask, render_template, request, redirect, session,jsonify,send_file,render_template_string
from flask import Flask, url_for,jsonify
from flask_socketio import SocketIO, emit
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

if __name__ == '__main__':
    water_temperature1, ph1, dissolved_oxygen, permanganate_index, ammonia_nitrogen, total_phosphorus, total_nitrogen = get_water_quality_data1()
       
    quality_standards = {
    "水温（℃）": [None, None, None, None, None],  # 需特殊处理
    "pH(无量纲)": [9, 9, 9, 9, 9],
    "溶氧量(mg/L)": [7.5, 6, 5, 3, 2],
    "高锰酸盐指数（mg/L）": [2, 4, 6, 10, 15],
    "氨氮（mg/L）": [0.15, 0.5, 1.0, 1.5, 2.0],
    "总磷（mg/L）": [0.02, 0.1, 0.2, 0.3, 0.4],
    "总氮（mg/L）": [0.2, 0.5, 1.0, 1.5, 2.0],
    
}

    row_data = {
            "水温（℃）": water_temperature1,
            "pH(无量纲)": ph1,
            "溶氧量(mg/L)": dissolved_oxygen,
            "高锰酸盐指数（mg/L）": permanganate_index,
            "氨氮（mg/L）": ammonia_nitrogen,
            "总磷（mg/L）": total_phosphorus,
            "总氮（mg/L）": total_nitrogen
        }

    for parameter, thresholds in quality_standards.items():
        value = row_data.get(parameter)
        print(type(value),type(thresholds[0]))

