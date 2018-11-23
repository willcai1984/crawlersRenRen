# -*- coding: utf-8 -*-
"""
    monitor.py
    ~~~~~~~~~~~~~~
    :copyright:...
"""
# from flask import Flask
# # 创建项目对象
# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)

from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


@app.route("/weixin/", methods=["GET", "POST"])
def index():
    if request.method == "GET":  # 判断请求方式是GET请求
        my_signature = request.args.get('signature')  # 获取携带的signature参数
        my_timestamp = request.args.get('timestamp')  # 获取携带的timestamp参数
        my_nonce = request.args.get('nonce')  # 获取携带的nonce参数
        my_echostr = request.args.get('echostr')  # 获取携带的echostr参数
        token = 'yiqian'  # 一定要跟刚刚填写的token一致
        # 进行字典排序
        data = [token, my_timestamp, my_nonce]
        data.sort()
        # 拼接成字符串
        temp = ''.join(data)
        # 进行sha1加密
        mysignature = hashlib.sha1(temp).hexdigest()
        # 加密后的字符串可与signature对比，标识该请求来源于微信
        if my_signature == mysignature:
            return my_echostr


if __name__ == "__main__":
    app.run()
