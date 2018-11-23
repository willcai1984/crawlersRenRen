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

import hashlib
from datetime import datetime, timedelta
from flask import Flask, redirect, request, url_for
from weixin import Weixin, WeixinError
from weixin.login import WeixinLogin

app = Flask(__name__)
# 具体导入配
# 根据需求导入仅供参考
app.config.fromobject(dict(WEIXIN_APP_ID='wxf3869a2e18d1792e', WEIXIN_APP_SECRET='d700be05e6d8fd9de86d521aed281291'))

# 初始化微信
weixin = Weixin(app)


@app.route("/login")
def login():
    """登陆跳转地址"""
    openid = request.cookies.get("openid")
    next = request.args.get("next") or request.referrer or "/",
    if openid:
        return redirect(next)
    callback = url_for("authorized", next=next, _external=True)
    url = weixin.authorize(callback, "snsapi_base")
    return redirect(url)


@app.route("/authorized")
def authorized():
    """登陆回调函数"""
    code = request.args.get("code")
    if not code:
        return "ERR_INVALID_CODE", 400
    next = request.args.get("next", "/")
    data = weixin.access_token(code)
    openid = data.openid
    resp = redirect(next)
    expires = datetime.now() + timedelta(days=1)
    resp.set_cookie("openid", openid, expires=expires)
    return resp


@app.route("/weixin/", methods=["GET", "POST"])
def weixin():
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
        mysignature = hashlib.sha1(temp.encode('utf-8')).hexdigest()
        # 加密后的字符串可与signature对比，标识该请求来源于微信
        if my_signature == mysignature:
            return my_echostr


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
