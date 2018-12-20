# -*- coding: utf-8 -*-
"""
    main.py
    ~~~~~~~~~~~~~~
    :copyright:...
"""
import os
import datetime
import traceback
import logging
from logging import handlers
from spiderrenren import SpiderRenren
from util import RandomPasswd
from util import ZipObj
from util import SQLProcess
from util import QCFile

if __name__ == '__main__':
    # 处理log
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
                                  datefmt="%m/%d/%Y %I:%M:%S %p")
    # 配置stdout
    console = logging.StreamHandler()  # 配置日志输出到控制台
    console.setLevel(logging.DEBUG)  # 设置输出到控制台的最低日志级别
    console.setFormatter(formatter)  # 设置格式
    logger.addHandler(console)
    # 配置file
    log_path = "crawlersrenren.log" if os.name == "nt" else "/var/log/py/crawlersrenren.log"
    file_rotating_file = handlers.RotatingFileHandler("crawlersrenren.log", maxBytes=1024, backupCount=5)
    file_rotating_file.setLevel(logging.INFO)
    file_rotating_file.setFormatter(formatter)
    logger.addHandler(file_rotating_file)

    sql = SQLProcess("localhost", "wechat", "wechat123", "wechat")
    q = QCFile()
    # 查询是否有正在进行中的进程
    sql1 = "select * from subscription_account where user_status=1 order by create_time;"
    r1 = sql.select(sql1)
    if r1:
        logger.info("还有爬取进程正在运行中，跳过此次轮循")
        os.system("0")
    else:
        # 查询待抓取的帐号，以创建时间的顺序排队抓取
        sql2 = "select id,open_id,user_name,user_pwd from subscription_account where user_status=0 order by create_time;"
        r2 = sql.select(sql2)
        if r2:
            logger.info("人人网爬取开始")
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
                logger.info("相册处理开始")
                # 处理相册部分
                photo_folder = s.get_photo()
                photo_passwd = RandomPasswd(12)
                z.enrypt_folder(photo_folder, photo_folder + '.zip', photo_passwd, True)
                photo_file_path = photo_folder + '.zip'
                photo_file_name = 'renren-' + photo_folder + '.zip'
                photo_r = q.upload_slice_file(photo_file_path, photo_file_name)
                photo_url = "https://yiqian-1253797768.cos.ap-shanghai.myqcloud.com/" + photo_file_name
                os.remove(photo_file_path)
                logger.info("日志处理开始")
                # 处理日志部分
                blog_folder = s.get_blog()
                blog_passwd = RandomPasswd(12)
                # print(blog_passwd)
                z.enrypt_folder(blog_folder, blog_folder + '.zip', blog_passwd, True)
                blog_file_path = blog_folder + '.zip'
                blog_file_name = 'renren-' + blog_folder + '.zip'
                blog_r = q.upload_slice_file(blog_file_path, blog_file_name)
                blog_url = "https://yiqian-1253797768.cos.ap-shanghai.myqcloud.com/" + blog_file_name
                os.remove(blog_file_path)
                # 查看detail表内是否有记录
                sql4 = "select * from subscription_accountdetail where account_id=%s;" % account_id
                r4 = sql.select(sql4)
                if r4:
                    logger.info("detail表内已有数据，进行更新操作")
                    # update
                    sql5 = "update subscription_accountdetail set blog_url='%s',blog_pwd='%s',photo_url='%s',photo_pwd='%s',update_time=%s where account_id=%s;" % (
                        blog_url, blog_passwd, photo_url, photo_passwd, datetime.datetime.now(), account_id)
                    logger.info(sql5)
                    r5 = sql.execute(sql5)
                else:
                    logger.info("detail表内无数据，进行插入操作")
                    # insert
                    sql6 = "INSERT INTO subscription_accountdetail  (account_id,open_id,blog_url,blog_pwd,photo_url,photo_pwd,is_pay,is_delete,create_time,update_time) VALUES (%s,'%s','%s','%s','%s','%s',%s,%s,'%s','%s');" % (
                        account_id, open_id, blog_url, blog_passwd, photo_url, photo_passwd, 0, 0,
                        datetime.datetime.now(), datetime.datetime.now())
                    logger.info(sql6)
                    r6 = sql.execute(sql6)
                    # 将对应account状态置为成功
                logger.info("detail表操作成功，更新account表状态为成功")
                sql7 = "update subscription_account set user_status=%s where id=%s;" % (2, account_id)
                logger.info(sql7)
                r7 = sql.execute(sql7)
            except Exception as e:
                # # 将对应account状态置为失败
                logger.error("爬取操作失败，抛出错误信息，更新account表状态为失败")
                logger.error(traceback.format_exc())
                sql8 = "update subscription_account set user_status=%s,desc='%s' where id=%s;" % (
                    3, traceback.format_exc(), account_id)
                logger.info(sql8)
                r8 = sql.execute(sql8)
        else:
            logger.info("无待爬取账户")
