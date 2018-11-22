# -*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~~~~~~~~
    :copyright:...
"""
from spider_renren import SpiderRenren
from util import RandomPasswd
from util import ZipObj

if __name__ == '__main__':
    user = "renggang@sina.com"
    passwd = "*****"
    s = SpiderRenren(user, passwd)
    z = ZipObj()
    photo_folder = s.get_photo()
    photo_passwd = RandomPasswd(16)
    print(photo_passwd)
    z.enrypt_folder(photo_folder, photo_folder + '.zip', photo_passwd, True)
    blog_folder = s.get_blog()
    blog_passwd = RandomPasswd(16)
    print(blog_passwd)
    z.enrypt_folder(blog_folder, blog_folder + '.zip', blog_passwd, True)
