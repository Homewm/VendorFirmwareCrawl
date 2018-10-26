# -*- coding:utf-8 -*-

"""针对ftp链接的固件下载模块"""

"""
 * @autor:zhangguodong
 * @Time:2018.08.20
 *
 * @File: ftpFiles_Download.py
 * @version: 1.0
 * @Function：***下载ftp://ftp2.dlink.com网址上的固件**
 * @Requires：（1）使用此脚本需要知道服务器地址或域名、用户名、密码。
              （2）针对此服务器地址ftp://ftp2.dlink.com的用户名必须为anonymous，密码任意。通过抓包分析得知用户名固定，密码不固定。
              （3）对于公开的不需使用用户名和密码的ftp地址，需要我们自己使用wireshark等抓包工具进行抓包获取用户名和密码。
              （4）使用时需要修改savePath函数的saveDir把文件保存路径和类内的__inint__函数内的self.conn.cwd内的服务器文件所在路径。
 * @Description:（1）针对ftp文件传输协议的文件和文件夹的递归下载，不同于http和https协议。
                    http和https的可以使用scrapy等框架爬取，而scrapy暂时还不支持ftp协议的，需要对scrapy开发扩展插件才能完成。
                （2）此脚本的目的在于能够递归地下载ftp文本传输协议的文件夹和文件内容。
                
"""


import os
import ftplib
import timeit
import multiprocessing
import threading


class FTPSync(object):
    def __init__(self, host = 'ftp2.dlink.com', user = 'anonymous', passwd = 'mozilla@example.com' ):
        ###抓包分析知针对ftp://ftp2.dlink.com网址的用户名固定，密码任意
        '''配置服务器连接，所需信息包括：域名或ip、用户名、密码'''
        self.conn = ftplib.FTP(host = host, user = user, passwd = passwd)
        self.conn.cwd('PRODUCTS/')     # 服务器端FTP目录
        # os.chdir('E:\\dlink')             # 本地的文件保存目录


    def get_files_dirs(self):
        '''获取当前目录和文件，返回当前文件夹下所有的文件和问价夹的列表'''
        dir_res = []
        self.conn.dir('.', dir_res.append)
        # print dir_res   ###['drwxr-xr-x 2 1001 1001 4096 Apr 20  2015 DCS-2132',...]

        files = []
        dirs = []
        try:
            for f in dir_res:
                if f.startswith('-'):
                    file = f.split(None, 8)[-1]   ###上面之间的空格必须使用None，而不能使用空格
                    files.append(file)

                elif f.startswith('d'):
                    dir = f.split(None, 8)[-1]
                    dirs.append(dir)

                else:
                    pass

        except Exception, e:
            raise e.message

        # files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        # dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return files, dirs


    def get_dirFile(self, next_dir):
        # print 'test_by_zgd:', next_dir

        self.conn.cwd(next_dir)

        try:
            os.mkdir(next_dir)

        except OSError:
            pass

        os.chdir(next_dir)
        # print os.getcwd()

        ftp_curr_dir = self.conn.pwd()    ###ftp上所在的当前文件夹 如：/BETA_FIRMWARE
        local_curr_dir = os.getcwd()      ###当前文件所在完整目录，如：G:\workspace\Vulnerability_Database

        files, dirs = self.get_files_dirs()
        # print "FILES: ", files
        # print "DIRS: ", dirs


        for f in files:
            #print next_dir, ':', f
            # os.path.abspath(f)
            print 'download :', os.path.abspath(f)    ###添加绝对路径，并打印输出
            # print os.path.getsize(f)
            if os.path.isfile(f):
                pass
            else:
                try:
                    outf = open(f, 'wb')
                    try:
                        self.conn.retrbinary('RETR %s' % f, outf.write)  ###下载文件
                    except Exception, e:
                        raise e.message
                    finally:
                        outf.close()
                except Exception, e:
                    raise e.message

        for d in dirs:
            os.chdir(local_curr_dir)        #切换本地的当前工作目录为d的父文件夹
            self.conn.cwd(ftp_curr_dir)     #切换ftp的当前工作目录为d的父文件夹
            self.get_dirFile(d)             #在这个递归里面，本地和ftp的当前工作目录都会被更改


    def run(self):
        self.get_dirFile('.')


def savePath():
    '''下载文件的本地保存位置'''
    saveDir = "E:\\dlink_by"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    else:
        pass
    os.chdir(saveDir)  ###os.chdir() 方法用于改变当前工作目录到指定的路径


def main():
    savePath()
    f = FTPSync()
    f.run()



if __name__ == '__main__':
    # main()
    start = timeit.default_timer()

    pool = multiprocessing.Pool(32)
    pool.apply(func = main)
    pool.close()
    pool.join()

    # for i in range(100):
    #     thread = threading.Thread(target = main)
    #     thread.start()

    end = timeit.default_timer()
    print "The file runs time is", str(end - start)
