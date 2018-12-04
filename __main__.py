# -*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~~~~~~~~
    :copyright:...
"""
import os
import datetime
from spiderrenren import SpiderRenren
from util import RandomPasswd
from util import ZipObj
from util import SQLProcess
from util import QCFile

if __name__ == '__main__':
    sql = SQLProcess("localhost", "wechat", "wechat123", "wechat")
    q = QCFile()
    # 查询是否有正在进行中的进程
    sql1 = "select * from subscription_account where user_status=1 order by create_time;"
    r1 = sql.select(sql1)
    if r1:
        print("还有爬取进程正在运行中，跳过此次轮循")
        os.system("0")
    else:
        # 查询待抓取的帐号，以创建时间的顺序排队抓取
        sql2 = "select id,open_id,user_name,user_pwd from subscription_account where user_status=0 order by create_time;"
        r2 = sql.select(sql2)
        if r2:
            print("进入爬取环节")
            account_id = r2[0][0]
            open_id = r2[0][1]
            user = r2[0][2]
            passwd = r2[0][3]
            try:
                # 将对应account的状态置为爬取中
                sql3 = "update subscription_account set user_status=%s where id=%s;" % (1, account_id)
                r3 = sql.execute(sql3)
                s = SpiderRenren(user, passwd)
                z = ZipObj()
                photo_folder = s.get_photo()
                photo_passwd = RandomPasswd(16)
                print(photo_passwd)
                z.enrypt_folder(photo_folder, photo_folder + '.zip', photo_passwd, True)
                photo_file_path = photo_folder + '.zip'
                photo_file_name = 'renren-' + photo_folder + '.zip'
                photo_r = q.upload_slice_file(photo_file_path, photo_file_name)
                photo_url = "https://yiqian-1253797768.cos.ap-shanghai.myqcloud.com/" + photo_file_name
                blog_folder = s.get_blog()
                blog_passwd = RandomPasswd(16)
                print(blog_passwd)
                z.enrypt_folder(blog_folder, blog_folder + '.zip', blog_passwd, True)
                blog_file_path = blog_folder + '.zip'
                blog_file_name = 'renren-' + blog_folder + '.zip'
                blog_r = q.upload_slice_file(blog_file_path, blog_file_name)
                blog_url = "https://yiqian-1253797768.cos.ap-shanghai.myqcloud.com/" + blog_file_name
                # 查看detail表内是否有记录
                sql4 = "select * from subscription_accountdetail where account_id=%s;" % account_id
                r4 = sql.select(sql4)
                if r4:
                    # update
                    sql5 = "update subscription_accountdetail set blog_url='%s',blog_pwd='%s',photo_url='%s',photo_pwd='%s',update_time=%s where account_id=%s;" % (
                        blog_url, blog_passwd, photo_url, photo_passwd, datetime.datetime.now(), account_id)
                    r5 = sql.execute(sql5)
                else:
                    # insert
                    sql6 = "INSERT INTO subscription_accountdetail  (account_id,open_id,blog_url,blog_pwd,photo_url,photo_pwd,is_pay,pay_serial_no,is_delete,create_time,update_time) VALUES (%s,'%s','%s','%s','%s','%s',%s,'%s',%s,'%s','%s');" % (
                        account_id, open_id, blog_url, blog_passwd, photo_url, photo_passwd, 0, '', 0,
                        datetime.datetime.now(), datetime.datetime.now())
                    r6 = sql.execute(sql6)
                    # 将对应account状态置为成功
                sql7 = "update subscription_account set user_status=%s where id=%s;" % (2, account_id)
                r7 = sql.execute(sql7)
            except Exception as e:
                # # 将对应account状态置为失败
                sql8 = "update subscription_account set user_status=%s where id=%s;" % (3, account_id)
                r8 = sql.execute(sql8)
        else:
            print("没有待爬取的帐户")
