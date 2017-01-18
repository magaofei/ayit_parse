#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import pymongo
from multiprocessing import Pool
import re

client = pymongo.MongoClient('localhost', 27017) #连接
ayit_news = client['ayit_news']  #数据库
news_list = ayit_news['news_list']   #表



# http://www.ayit.edu.cn/xwzx/agyw.htm
url_import_list = 'http://www.ayit.edu.cn/xwzx/agyw.htm'
url_trends_list = 'http://www.ayit.edu.cn/xwzx/ybdt.htm'


def news_url_first(url, is_usedb):
    wb_data = requests.get(url)
    wb_data.encoding = 'utf-8'
    soup = BeautifulSoup(wb_data.text, 'lxml')

    titles = soup.select('div.newslist.l > ul > li > a')
    # times = soup.select('span.time')
    pages_number = soup.select('td#fanye126886')

    # print(titles)
    tag = ''
    try:
        for title in titles:
            if (title.get('href').find('www.ayit.edu.cn')):
                info = {
                    'title': title.text.split('[')[0],
                    'time': title.text.split('[')[-1].rstrip(']'),
                    # if (title.get('href'))
                    'url': 'http://www.ayit.edu.cn' + title.get('href').lstrip('..'),  # 删掉前面的两个..
                    'tag': url.split('/')[-1].rstrip('htm').strip('.')   # 判断是哪一部分的新闻
                }
                tag = info['tag']
                if (is_usedb == True):
                    news_list.insert_one(info)
                print(info)

        number_info = ''
        for number in pages_number:
            string = number.text.split('/')[-1]
            # number_info = {
            #     'pages_number': re.findall(r"\d+\.?\d*",string)
            # }
            number_info = re.findall(r"\d+\.?\d*",string)


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
        numbers = number_info[0]

    # 这里不知为何，不能同时删除. 和 htm 否则会多删一个
        url_list = [url.rstrip('htm').rstrip('.') + '/{}.htm'.format(str(i)) for i in range(int(numbers) - 1, 0, -1)]
    except:
        pass


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
                        news_list.insert_one(info)
                    print(info)
        except:
            pass


news_url_first(url_import_list, False)



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





