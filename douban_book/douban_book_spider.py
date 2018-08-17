# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 18:04
# @Author  : 银河以北
# @Email   : smilegks@163.com
# @Introduction   : 爬取豆瓣图书，共36*4个标签，每个标签下爬取5页，每页20条数据（共爬取 36*4*5*20=14400条数据）
# 爬取2万条数据后被豆瓣封了ip。。。。。

import requests
from bs4 import BeautifulSoup
import re
import time, random
import datetime

def download_page(url, headers):
    r = requests.get(url, headers=headers)
    return r.text

def get_header():
    '''
    随机获取一个User-Agent
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

def get_list_urls(html_text):
    '''
    获取图书标签，然后构造每个标签的列表url
    :param html_text:
    :return:返回一个list：构造的url列表 label_urls
    '''
    soup = BeautifulSoup(html_text, 'html.parser')
    # 获取豆瓣图书标签,放在列表L中
    L = soup.select('.tagCol a')
    # 使用标签造url，将造的url循环添加到list中
    label_urls = []
    for l in L:
        label_url = "https://book.douban.com/tag/" + str(l.get_text())
        label_urls.append(label_url)

    return label_urls

def get_content(html_text):
    '''
    获取图书信息，并保存到csv文件中
    :param html_text:
    :return:
    '''
    soup = BeautifulSoup(html_text, 'html.parser')
    con = soup.find(class_='subject-list')
    # 获取每一条信息，放在列表中
    con_list = con.find_all('li', class_='subject-item')
    for i in con_list:
        # 图书name
        book_name = i.find('h2').get_text().replace(" ","").replace("\n", "")
        # 图书url
        book_url = i.find('h2').a['href']
        # 图书信息
        book_info = i.find(class_='pub').get_text().strip().replace("\n", "")

        # # 图书简介
        # book1 = i.find('p')
        # # 有的图书没有简介
        # if book1 is not None:
        #     book_introduction = book1.get_text().replace(" ","").replace("\n", "")
        # else:
        #     # 没有简介时，简介设为空
        #     book_introduction = "无"

        # 评分和评论总人数
        # 少于10人评价时，没有评分和评价人数
        rating = i.find('span', class_='rating_nums')
        if rating is not None:
            # 评分
            rating_nums = i.find('span', class_='rating_nums').get_text().strip().replace("\n", "")
            # 评价总人数：(17455人评价)
            comment = i.find('span', class_='pl').get_text().strip().replace("\n", "")
            # 使用re模块的正则提取出数字：17455 ，re.findall()返回的是list
            comment_nums = re.findall("\d+", comment)[0]
        else:
            # 少于10人评价，评分为空，评价人数="少于10人评价"
            rating_nums = ""
            comment_nums = "少于10人评价"

        # 将数据写入csv
        with open("data\douban_book.csv", "a", encoding='utf-8') as f:
            f.write("{},,,{},,,{},,,{},,,{}\n".format(book_name, book_url, book_info, rating_nums, comment_nums))

def pachong_log(log_info):
    '''
    打印当前系统时间和日志信息到txt中。
    :param log_info: 想要打印的信息
    :return:
    '''
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("data\log.txt", "a", encoding='utf-8') as f:
        f.write(nowtime + "  " + log_info)
        f.close()


if __name__ == '__main__':
    headers = get_header()
    # 爬取图书标签，使用标签构造列表url
    html1 = download_page('https://book.douban.com/tag/?view=type&icn=index-sorttags-all', headers)
    urls_list = get_list_urls(html1)
    for u in urls_list:
        # 打印日志
        log1 = "***开始爬取：{}\n".format(u)
        print(log1)
        pachong_log(log1)
        for m in range(1, 6):
            url1 = u + "?start={}&type=T".format(0 + 20 * (m - 1))
            headers = get_header()
            html2 = download_page(url1, headers)
            get_content(html2)
            # 打印日志
            log2 = "第{}页数据爬取完成\n".format(m)
            print(log2)
            pachong_log(log2)
            # 设置随机等待时间，防止被封，同时降低被爬取网站的压力
            time.sleep(random.random()*3)
