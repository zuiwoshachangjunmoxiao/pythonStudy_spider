# -*- coding: utf-8 -*-
# @Time    : 2018/8/16 18:33
# @Author  : 银河以北
# @Email   : smilegks@163.com
# @Introduction   : 爬取豆瓣电影全部类型下，按热度排序，前200页（4000部）电影的初步信息。

import requests
import time, random
import datetime

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

# 拼接出前200页的url
for m in range(1,201):
    url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}".format(20*(m-1))
    r = requests.get(url)
    # 返回的json文件，所以是 r.json()，而不是 r.text
    t = r.json()
    # 打印日志
    log1 = "第{}页爬取开始...\n".format(m)
    print(log1)
    pachong_log(log1)

    # 获取电影信息
    dict1 = t['data']
    # json 内容中电影的数量
    num = len(dict1)
    for i in range(num):
        # 取出列表 data 中第 i 部电影的信息，一部电影的信息就是一个字典 dict
        dict = t['data'][i]
        # 电影名
        title = dict['title']
        # 电影详情url
        url = dict['url']
        # 导演,可能有多个导演，返回list
        directors = dict['directors']
        # 主演，可能有多个，返回list
        casts = dict['casts']
        # 评分
        rate = dict['rate']
        # 封面图片地址
        cover = dict['cover']
        # id
        id = dict['id']
        # 其他信息
        star = dict['star']
        cover_x = dict['cover_x']
        cover_y = dict['cover_y']
        # 保存到csv文件中
        with open("data\douban_moive.csv", "a", encoding='utf-8') as f:
            f.write("{},,,{},,,{},,,{},,,{},,,{},,,{},,,{},,,{},,,{}\n".format(title, url, "、".join(directors), "、".join(casts), rate, cover, id, star, cover_x, cover_y))
    # 暂停随机时间
    time.sleep(random.random()*3)
    # 打印日志
    log2 = "第{}页爬取完成，该页共爬取{}部电影\n".format(m, num)
    print(log2)
    pachong_log(log2)


