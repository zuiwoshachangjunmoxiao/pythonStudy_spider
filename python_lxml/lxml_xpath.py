# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:57
# @Author  : 银河以北
# @Email   : smilegks@163.com
# @Introduction   :
'''
python + lxml 爬虫，以豆瓣图书为例，爬取豆瓣图书的信息。
Python 3.6.5
安装 lxml 库，安装有点复杂（可能出错）。我使用的Anaconda3，自带lxml 4.3.1，不需要自己安装，推荐使用。
'''

import requests
from lxml import etree

# 要爬取的URL
url = "https://book.douban.com/tag/%E5%8E%86%E5%8F%B2"

# 1、下载网页
# 使用requests下载网页，然后用lxml解析。
r = requests.get(url)
# 注意使用r.content，使用r.text会报错。r.text返回的是Unicode型数据，r.content返回的是bytes型数据。
response = r.content


# 2、解析网页
'''
etree.fromstring()  # 用于解析字符串
etree.HTML()        # 用于解析HTML对象
etree.XML()         # 用于解析XML对象
etree.parse()       # 用于解析文件类型的对象，parse{帕斯]=解析
'''
htmlElement = etree.HTML(response)  # 返回值为对象
# 构建 DOM 树。 使用tostring decode，格式化html代码。
html = etree.tostring(htmlElement, encoding='utf-8').decode('utf-8')  # 返回值为str


# 3、定位
# 图书信息列表
bookinfo_list = htmlElement.xpath('//*[@id="subject_list"]/ul/li')  # 返回值是list，list中元素是一个个对象

'''
str.strip() 去掉行首行尾的空白字符，包括空格、\t、\r、\n
str.lstrip() 去掉行首(str左侧)的空白字符，包括空格、\t、\r、\n
str.rstrip() 去掉行首(str右侧)的空白字符，包括空格、\t、\r、\n
'''

for book in bookinfo_list:
    # 图书名称
    # 图书名称包括主标题和副标题，同时显示主标题和副标题需要处理一下。
    #book_name = book.xpath('.//div[2]/h2/a/text()')[0].strip()
    book_a = book.xpath('.//div[2]/h2/a')
    children = book_a[0].getchildren()
    if len(children):
        # 如果 a 标签的子节点存在，图书名称就加上子节点中的副标题
        book_name = book_a[0].text.strip() + children[0].text.strip()
    else:
        book_name = book_a[0].text.strip()

    # 图书详情URL
    bookinfo_url = book.xpath('.//div[2]/h2/a/@href')[0]
    # 基本信息
    book_baseinfo = book.xpath('.//div[2]/div[1]/text()')[0].strip()
    # 评分
    rating = book.xpath('.//div[2]/div[2]/span[2]/text()')[0]
    # 评论人数
    rate_nums = book.xpath('.//div[2]/div[2]/span[3]/text()')[0].strip().replace('人评价','').replace('(','').replace(')','')
    # 封面URL
    fengmian_url = book.xpath('.//div[1]/a/img/@src')[0]
    # 图书简介
    #book_instr = book.xpath('.//div[2]/p/text()')[0]

    # 打印爬取的信息
    print("{},{},{},{},{},{}".format(book_name, bookinfo_url, book_baseinfo, rating, rate_nums, fengmian_url))

    # 将数据写入csv
    with open("data\douban_book.csv", "a", encoding='utf-8') as f:
        f.write("{},{},{},{},{},{}\n".format(book_name, bookinfo_url, book_baseinfo, rating, rate_nums, fengmian_url))