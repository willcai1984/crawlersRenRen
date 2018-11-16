# -*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~~~~~~~~
    :copyright:...
"""
# 导入需要的模块
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 登录人人网的url
    url0 = "http://www.renren.com/PLogin.do"
    # 登录到个人主页的url
    url1 = "http://www.renren.com/962817283/profile"
    data = {'email': "renggang@sina.com",
            'password': 'renren1234'}
    # 进行登录，并保存cookie
    req = requests.Session()
    login_res = req.post(url0, data=data)
    # 获取个人ID及信息
    login_bs = BeautifulSoup(login_res.text, "html.parser")
    home_element = login_bs.select('.hd-name')[0]
    home_url = home_element.get('href')
    # 可以直接访问个人主页了
    home_res = req.get(home_url)
    home_bs = BeautifulSoup(home_res.text, "html.parser")
    # 获取日志
