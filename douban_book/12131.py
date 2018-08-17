# -*- coding: utf-8 -*-
# @Time    : 2018/8/14 16:31
# @Author  : 银河以北
# @Email   : smilegks@163.com
# @Introduction   : 尝试试用代理和随机选择user-Agent

import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import random

url = 'https://www.baidu.com/'
# 在https://proxy.coderbusy.com/找到的IP地址（不停刷新即可）
# # pro = [
# '178.128.10.38:3128',
# '189.198.226.14:53281',
# '159.203.176.16:8080']
# r = requests.get(url, proxies={'http':random.choice(pro)}, stream=True)
# print(r.raw._connection.sock.getpeername()[0])
# print(r.raw._connection.sock.getsockname()[0])

def get_proxies():
    '''
    随机获取一个代理
    :return:
    '''

    pro = []

def get_header():
    '''
    随机获取一个header
    :return:
    '''
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0)',
        'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
        'Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
    ]

    headers = {'User-Agent': random.choice(user_agents)}
    return headers


if __name__ == '__main__':
    proxies = {
        'http': 'http://101.236.51.35:8866',
        'https': 'http://115.223.70.236:8010',
    }

    headers = get_header()
    #r = requests.get(url, headers=headers, proxies=proxies, stream=True)
    r = requests.get(url, proxies=proxies)
