#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import pymongo
from multiprocessing import Pool
import re
import time, os

client = pymongo.MongoClient('localhost', 27017) #连接
ayit_news = client['ayit_news']  #数据库

table_news_import = ayit_news['news_import']   #表
table_news_trends = ayit_news['news_trends']   #表
table_news_affiche = ayit_news['news_affiche']   #表
table_news_science = ayit_news['news_science']   #表



# http://www.ayit.edu.cn/xwzx/agyw.htm
url_import_list = 'http://www.ayit.edu.cn/xwzx/agyw.htm'
url_trends_list = 'http://www.ayit.edu.cn/xwzx/ybdt.htm'
url_affiche_list = 'http://www.ayit.edu.cn/xwzx/tzgg.htm'
url_science_list = 'http://www.ayit.edu.cn/xwzx/xsxx.htm'




def news_url_first(news_url, is_usedb):
    wb_data = requests.get(news_url)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, 'lxml')

    titles = soup.select('div.newslist.l > ul > li > a')
    # times = soup.select('span.time')
    pages_number = soup.select('td#fanye126886')


    # print(titles)
    tag = ''
    try:
        # 先删除，再添加数据
        if (is_usedb == True):

            news_delete(news_url)

        for title in titles:
            if (title.get('href').find('www.ayit.edu.cn')):
                info = {
                    'title': title.text.split('[')[0],
                    'time': title.text.split('[')[-1].rstrip(']'),
                    # if (title.get('href'))
                    'url': 'http://www.ayit.edu.cn' + title.get('href').lstrip('..'),  # 删掉前面的两个..
                    'tag': news_url.split('/')[-1].rstrip('htm').strip('.')   # 判断是哪一部分的新闻
                }
                tag = info['tag']
                if (is_usedb == True):
                    # 这里判断传入的是哪个网址，然后插入相关的表
                    if (news_url == url_import_list):
                        table_news_import.insert_one(info)
                    elif (news_url == url_trends_list):
                        table_news_trends.insert_one(info)
                    elif (news_url == url_affiche_list):
                        table_news_affiche.insert_one(info)
                    elif (news_url == url_science_list):
                        table_news_science.insert_one(info)
                elif (is_usedb == False):
                    print(info)
                    # if (news_exist(info)== True):
                    #     print('没有新数据')
                    #     pass
                    # elif ((news_exist(info)== False)):
                    #     print('insert')
                    #     pass
                    #     news_list.insert_one(info)



        # 未实现功能， 每次在插入时 对数据库做一次查询 如果有就不增加

        # if (is_usedb == True):
        #     for i in news_list.find().limit(400):
        #         print(info['title'])
                # if (i['title'] == info['title']):
                #     print('相同')


    except:
        pass


    number_info = ''
    for number in pages_number:
        string = number.text.split('/')[-1]
        # number_info = {
        #     'pages_number': re.findall(r"\d+\.?\d*",string)
        # }
        number_info = re.findall(r"\d+\.?\d*", string)

        # print(string)

        # news_url(info['pages_number'])
    #
    # # if (url == url_import_list):  # 第一次
    # number = number_info['pages_number']
    # for i in range(int(number) - 1, 0 , -1):
    #     url_list = [url.rstrip('.htm') + '/{}.htm'.format(str(i))]
    #
    # for url in url_list:
    #         news_url_first(url)

    # numbers = number_info['pages_number']




    numbers = int(number_info[0])
    url_list = [news_url.rstrip('htm').rstrip('.') + '/{}.htm'.format(str(i)) for i in range(numbers - 1, 0, -1)]
    # 这里不知为何，不能同时删除. 和 htm 否则会多删一个


    # 先删除，再添加数据
    # if (is_usedb == True):
    #     news_delete(url)

    # 查询到页码后 开始后面的遍历
    for url in url_list:
        # print(url)
        # news_url(url)
        wb_data = requests.get(url)
        wb_data.encoding = 'utf-8'  # 转为utf-8
        soup = BeautifulSoup(wb_data.text, 'lxml')

        titles = soup.select('div.newslist.l > ul > li > a')

        # print(titles)
        try:
            for title in titles:
                if (title.get('href').find('www.ayit.edu.cn')):

                    info = {
                        'title': title.text.split('[')[0],
                        'time': title.text.split('[')[-1].rstrip(']'),
                        # if (title.get('href'))
                        'url': 'http://www.ayit.edu.cn/' + title.get('href').lstrip('..').strip('/..'),  # 删掉前面的两个..
                        'tag': tag  # 判断是哪一部分的新闻
                    }
                    if (is_usedb == True):
                        if (news_url == url_import_list):
                            table_news_import.insert_one(info)
                        elif (news_url == url_trends_list):
                            table_news_trends.insert_one(info)
                        elif (news_url == url_affiche_list):
                            table_news_affiche.insert_one(info)
                        elif (news_url == url_science_list):
                            table_news_science.insert_one(info)
                    elif (is_usedb == False):
                        print(info)
        except:
            pass

# 查询数据是否存在，返回True 说明数据库已经有，返回False 说明数据库没有
def news_exist(info):
    # False 没有新数据

    for i in news_list.find():
        if (i['url'] == info['url']):
            # print(info)
            return True
        else:
            pass
            print('news_exist')
            # print(info)
            # return False

# 根据传入的url，删除所有数据
def news_delete(url):
    if (url == url_import_list):
        for i in table_news_import.find():
            table_news_import.delete_one(i)
    elif (url == url_trends_list):
        for i in table_news_trends.find():
            table_news_trends.delete_one(i)
    elif (url == url_affiche_list):
        for i in table_news_affiche.find():
            table_news_affiche.delete_one(i)
    elif (url == url_science_list):
        for i in table_news_science.find():
            table_news_science.delete_one(i)

#
#
#  默认60秒执行一次 , 传入是否要操作数据库的参数
i = 0

def re_exe(inc = 60, is_usedb = False):
    while True:
        # os.system(cmd)
        news_url_first(url_import_list, is_usedb)
        news_url_first(url_trends_list, is_usedb)
        news_url_first(url_affiche_list, is_usedb)
        news_url_first(url_science_list, is_usedb)

        i = i+1
        print(i)

        time.sleep(inc)

# 每3000秒执行一次
re_exe(30, True)
# news_url_first(url_import_list, True)
# news_delete()




# def news_url(url):
#     # 从number -1 页 到第1页 依次递减
#     # url_list = ['http://www.ayit.edu.cn/xwzx/agyw/{}.htm'.format(str(i)) for i in range(int(number)-1, 0, -1)]
#     wb_data = requests.get(url)
#     wb_data.encoding = 'utf-8'   # 转为utf-8
#     soup = BeautifulSoup(wb_data.text, 'lxml')
#
#     titles = soup.select('div.newslist.l > ul > li > a')
#
#     # print(titles)
#
#     for title in titles:
#         if (title.get('href').find('www.ayit.edu.cn')):
#             info = {
#                 'title': title.text.split('[')[0],
#                 'time': title.text.split('[')[-1].rstrip(']'),
#                 # if (title.get('href'))
#                 'url': 'http://www.ayit.edu.cn/' + title.get('href').lstrip('..').strip('/..'),  # 删掉前面的两个..
#                 'tag': url.split('/')[-1].rstrip('htm').strip('.')  # 判断是哪一部分的新闻
#             }
#         # news_list.insert_one(info)
#             print(info)




 # 数据有重复





