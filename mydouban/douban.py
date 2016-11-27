# -*- coding: utf-8 -*-
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import requests
import re
import time
import os.path
from bs4 import BeautifulSoup
try:
    from PIL import Image
except:
    pass

#构造 请求头
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'User-Agent': agent
}

#使用登录cookie信息
session = requests.session()
session.cookies =cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print ("Cookie未能加载")


def isLogin():
    url = "https://www.douban.com/accounts"
    login_returncode = session.get(url, allow_redirects=False).status_code
    if int(x=login_returncode) == 200:
        return True
    else:
        return False

# 获取验证码
def get_captcha(captcha_url):
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.close()
        f.write(r.content)
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = raw_input("please input the captcha\n>")
    return captcha

def get_captchaid():
    pass

# 登录
def login(account, password):
    print "尝试登录"
    post_url = 'https://accounts.douban.com/login'
    doubenloginhtml = session.get(post_url, headers=headers).content
    try:
        print "尝试使用验证码登录"
        #这里获取验证码是会失败的，失败就不用验证码登录
        # 获取验证码ID
        # 这边html解析好像有警告错误
        doubenlogin_captchaid = BeautifulSoup(doubenloginhtml).find('img', attrs={'name': 'captcha-id'})['value']
        # 获取验证码URL
        doubenlogin_captchaurl = BeautifulSoup(doubenloginhtml).find('input', attrs={'id': 'captcha_image'})['value']
        # 获取输入的验证码
        captchasolution = get_captcha(doubenlogin_captchaurl)
        postdata = {
            'source': 'book',
            'form_email': account,
            'form_password': password,
            'captcha-solution': captchasolution,
            'captcha-id': doubenlogin_captchaid,
            'remember': 'on',
        }
    except:
        print "尝试不使用验证码登录"
        #失败了尝试用验证码登录
        postdata = {
            'source': 'book',
            'form_email': account,
            'form_password': password,
            'remember': 'on',
        }
    # 提交申请
    sessionresponse = session.post(post_url, data=postdata, headers=headers)
    if sessionresponse.status_code == 200:
        print sessionresponse.content
        # 保存cookies
        session.cookies.save()
        return True
    else:
        return False

# 登录初始化接口
# 已经登录了直接返回成功
# 没有登录过会尝试登录,登录成功返回成功
def logininit(acount, password):
    # 参数检查
    if isinstance(acount, str) == False:
        raise TypeError("acount 传入非字符串")
    if isinstance(password, str) == False:
        raise TypeError("password 传入非字符串")
    if isLogin():
        print('您已经登录')
        return True
    else:
        if login("1223108078@qq.com", "taokai.123") == True:
            print "登录成功"
            return True
        else:
            print "登录失败"
            return False

if __name__ == '__main__':
    pass
    # 测试用例
    #logininit("1223108078@qq.com", "taokai.123")