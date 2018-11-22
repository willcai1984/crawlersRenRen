# -*- coding: utf-8 -*-
"""
    util.py
    ~~~~~~~~~~~~~~
    :copyright:...
"""
import random

import subprocess
import zipfile as zf
import platform as pf
import os
import re
import shutil


# 无法加密
class ZipProcess(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def zip_dir(self, dirname, zipfilename, passwd=''):
        # dirname 要压缩的文件夹路径
        # zipfilename 压缩后文件夹的名字
        with zf.ZipFile(zipfilename, 'w', zf.ZIP_DEFLATED) as z:
            for dirpath, dirnames, filenames in os.walk(dirname):
                fpath = dirpath.replace(dirname, '')  # 这一句很重要，不replace的话，就从根目录开始复制
                fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
                for filename in filenames:
                    z.write(os.path.join(dirpath, filename), fpath + filename)
                    # print('压缩成功')
            if passwd:
                # 如果不加bytes utf-8，会出现TypeError: pwd: expected bytes, got str,压缩加密无效，只能用于解密
                z.setpassword(bytes(passwd, encoding="utf8"))
            z.close()


class ZipObj(object):

    def __init__(self):
        pass

    def encrypt_file(self, file, passwd, is_delete=False):
        """
            压缩加密文件，并删除原数据
            window系统调用rar程序
            linux等其他系统调用内置命令 zip -P123 tar source
            默认不删除原文件
        """
        target = re.split('\.', file)[0] + ".zip"
        source = file
        if pf.system() == "Windows":
            cmd = ['rar', 'a', '-p%s' % passwd, target, source]
            p = subprocess.Popen(cmd, executable=r'C:\Program Files\WinRAR\WinRAR.exe')
            p.wait()
        else:
            cmd = ['zip', '-P %s' % passwd, target, source]
            p = subprocess.Popen(cmd)
            p.wait()
        if is_delete:
            os.remove(source)

    def enrypt_folder(self, dirname, zipfilename, passwd, is_delete=False):
        """
            压缩加密，并删除原数据
            window系统调用rar程序
            linux等其他系统调用内置命令 zip -P123 tar source
            默认不删除原文件
        """
        current_path = "C:\Works\Projects\Python\crawlersRenRen"
        if pf.system() == "Windows":
            # cmd = '''runas /savecred /user:Administrator "C:\Program Files\WinRAR\\rar a -p%s -r %s %s"''' % (
            # passwd, current_path + os.sep + zipfilename, current_path + os.sep + dirname)
            # p = subprocess.Popen(cmd, shell=True)
            # p = subprocess.Popen(cmd, executable=r'C:\Program Files\WinRAR\WinRAR.exe')
            p = subprocess.Popen('runas /savecred /user:Administrator cmd', shell=True)
            p = subprocess.Popen('cd %s' % current_path, shell=True)
            cmd = ['rar', 'a', '-p%s' % passwd, zipfilename, dirname]
            p = subprocess.Popen(cmd, executable=r'C:\Program Files\WinRAR\WinRAR.exe')
            p.wait()
        else:
            cmd = ['zip', '-r', '-P %s' % passwd, zipfilename, dirname]
            p = subprocess.Popen(cmd)
            p.wait()
        if is_delete:
            # os.remove(dirname)
            shutil.rmtree(dirname)

    def deCrypt(self):
        """
        使用之前先创造ZipObj类
        解压文件
        """
        zfile = zf.ZipFile(self.filepathname + ".zip")
        zfile.extractall(r"zipdata", pwd=self.passwd.encode('utf-8'))


# 随机生成密码
def RandomPasswd(rang=None):
    __numlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'q', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'W', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z']
    if rang == None:
        _Passwd = "".join(random.choice(__numlist) for i in range(8))
    else:
        _Passwd = "".join(random.choice(__numlist) for i in range(int(rang)))
    return _Passwd
