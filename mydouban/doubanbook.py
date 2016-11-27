# -*- coding: utf-8 -*-
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import requests
import time
import urllib
from bs4 import BeautifulSoup

try:
    from PIL import Image
except:
    pass
import dbaccbook
# 设置编码
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 构造 请求头
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print ("Cookie未能加载")


def geturlhtml(url):
    # 稍微休息那么一下
    time.sleep(1)
    # 请求页面
    # 处理一下请求时的异常
    # 请求三次都失败就不用尝试了
    bookpage_html = None
    trynum = 0
    while (trynum < 3):
        trynum += 1
        try:
            bookpage = session.get(url, headers=headers)
            if bookpage.status_code == 200:
                bookpage_html = bookpage.content
                break
            else:
                continue
        except:
            bookpage_html = None
            continue
    return bookpage_html

def formatstr(string=None):
    if string != None:
        return string.lstrip()
    else:
        return '无'

# 传入图书标签获取图书列表
def book_spider(book_tag):
    page_num = 0
    page_type = "T"
    while (True):
        # 拼接URL
        url_page = 'https://book.douban.com/tag/' + urllib.quote(book_tag) + '?start=' + str(
            page_num * 20) + '&type=' + page_type
        # 请求HTML页面
        bookpage_html = geturlhtml(url_page)
        # 假如获取的HTML界面为空那么下面的操作就没有必要了
        if bookpage_html == None:
            continue

        # 查找所有的书籍标签
        soup = BeautifulSoup(bookpage_html)
        try:
            list_soup = soup.find_all('li', {'class': 'subject-item'})
        except:
            continue

        # 解析查找到的书籍标签
        for book_info in list_soup:
            try:
                # info div
                bookinfo_div = book_info.find('div', {'class': 'info'})
                bookinfo_info_a = bookinfo_div.find('a')
                # 书名
                book_title = dict(bookinfo_info_a.attrs)['title']
                # 书链接
                book_url = dict(bookinfo_info_a.attrs)['href']

                # pub div
                bookpub_div = book_info.find('div', {'class': 'pub'})
                bookpub_content = bookpub_div.string
                bookpub_info_list = bookpub_content.split('/')
                # 翻译书籍
                if len(bookpub_info_list) == 5:
                    book_author = bookpub_info_list[0]
                    book_translator = bookpub_info_list[1]
                    book_public = bookpub_info_list[2]
                    book_time = bookpub_info_list[3]
                    book_price = bookpub_info_list[4]
                else:
                    # 无翻译书籍
                    book_author = bookpub_info_list[0]
                    book_public = bookpub_info_list[1]
                    book_time = bookpub_info_list[2]
                    book_price = bookpub_info_list[3]
                # star clearfix div
                bookstarclearfix_div = book_info.find('div', {'class': 'star clearfix'})
                bookstarclearfix_span = bookstarclearfix_div.find('span', {'class': 'rating_nums'})
                book_score = bookstarclearfix_span.string

                # summary p
                booksummary_p = book_info.find('p')
                book_summary = booksummary_p.string
            except:
                pass
            # 插入数据库
            dbaccbook.dbaccbook_insertrecord(bookurl=formatstr(book_url), bookname=formatstr(book_title), bookauthor=formatstr(book_author),
                                             booktranslate=formatstr(book_translator), bookpublic=formatstr(book_public), booktime=formatstr(book_time),
                                             bookprice=formatstr(book_price), bookscore=formatstr(book_score),
                                             booksubject=formatstr(book_summary), booktag=formatstr(book_tag))
        # 退出条件
        if len(list_soup) < 1:
            break
        # 加页数
        page_num += 1


if __name__ == '__main__':
    dbaccbook.dbaccbook_initdb()
    book_spider('演艺')
    pass
