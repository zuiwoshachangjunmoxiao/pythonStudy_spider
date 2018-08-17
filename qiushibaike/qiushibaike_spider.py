# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 13:55
# @Author  : 银河以北
# @Email   : smilegks@163.com
# @Introduction   : 第一次尝试，爬去糗事百科的内容，保存到txt中。

import requests
from bs4 import BeautifulSoup

def download_page(url):
    r = requests.get(url)
    return r.text

def get_content(html_text, page_num):
    '''
    :param html_text: 页面的源码
    :param page_num: 第几页
    :return:
    '''
    # 解析源码
    soup = BeautifulSoup(html_text, 'html.parser')
    con = soup.find(id='content-left')
    # 获取div列表
    con_list = con.find_all('div', class_='article')

    # 循环获取每一条数据
    for i in con_list:
        # 作者
        author = i.find('h2').string.strip()
        # 内容
        content = i.find('div', class_='content').find('span').get_text()
        # 作者信息：年龄、性别
        author_info = i.find('div', class_='articleGender')
        if author_info is not None:
            age = author_info.string
            m = author_info['class']
            if 'manIcon' in m:
                gender = "男"
            elif 'womenIcon' in m:
                gender = '女'
            else:
                gender = ''
        else:  # 匿名用户,性别、年龄为空
            gender = ''
            age = ''
        # 点赞
        vote = i.find('span', class_='stats-vote').find('i', class_='number').string
        # 评论
        comment = i.find('a', class_='qiushi_comments').find('i', class_='number').string

        # 将爬去的数据写入txt， 用"a" 的方式追加
        fo = open("qiushibaike.txt", "a", encoding='utf-8')
        fo.write("第{}页，作者：{}，性别：{}，年龄：{}，点赞数：{}，评论数：{}\n{}".format(page_num, author, gender, age, vote, comment, content))
        fo.write("--------------------------------------------------------------------------------------------------\n")


if __name__ == '__main__':
    for i in range(1,14):
        base_url = 'https://www.qiushibaike.com/text/page/{}'.format(i)
        content = download_page(base_url)
        get_content(content, i)
        print("第{}页爬取完成...".format(i))