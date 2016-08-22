# -*- coding: utf-8 -*-
import urllib2, urllib, cookielib, re, time

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US, en;q = 0.5',
    'Connection': 'keep-alive',
    'Cookie': '_gscu_1103646635=69155042d0dour98; _gscs_1103646635=69155042wyvvcb98|pv:1; _ga=GA1.3.234722701.1469155052; _gat=1',
    'Host': 'mis.teach.ustc.edu.cn',
    'User-Agent': 'Mozilla/5.0(X11;Ubuntu;Linux x86_64;rv:47.0) Gecko/20100101 Firefox/47.0'
}
# 进入主页，模拟 Ubuntu 16.04 + Firefox 47.0 登录，并获取 Cookie
url = 'http://mis.teach.ustc.edu.cn'
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
req = urllib2.Request(url, None, headers)
response = urllib2.urlopen(req)
jsessionid = response.info().getheader('Set-Cookie')
headers['Cookie'] = jsessionid
headers['Referer'] = 'http://mis.teach.ustc.edu.cn/'
data = {'userbz': 's'}
data = urllib.urlencode(data)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
compressedData = response.read()
# 尚不清楚date的用处，但是可以一直使用如下值
date = '1469242601259'
url = 'http://mis.teach.ustc.edu.cn/randomImage.do?date=%%27%s%%27' % date
headers['Accept'] = '*/*'
headers['Referer'] = 'http://mis.teach.ustc.edu.cn/userinit.do'
data = {'date': date}
data = urllib.urlencode(data)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
response.read()
# 提交用户名，密码和验证码，模拟登录
url = 'http://mis.teach.ustc.edu.cn/login.do'
data = {
    'check': '<checkcode>',  # checkcode,
    'passWord': '<passwd>',  # passwd,
    'userCode': '<username>',  # username,
    'userbz': 's'
}
data = urllib.urlencode(data)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
# 请求左侧边栏内容
url = 'http://mis.teach.ustc.edu.cn/left.do'
headers['Referer'] = 'http://mis.teach.ustc.edu.cn/login.do'
req = urllib2.Request(url, None, headers)
urllib2.urlopen(req)
# 模拟点击左侧边栏的选课按钮
url = 'http://mis.teach.ustc.edu.cn/init_xk_ts.do'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
headers['Referer'] = 'http://mis.teach.ustc.edu.cn/left.do'
req = urllib2.Request(url, None, headers)
urllib2.urlopen(req)
# 模拟点击“进入选课”按钮
url = 'http://mis.teach.ustc.edu.cn/init_st_xk_dx.do'
headers['Referer'] = 'http://mis.teach.ustc.edu.cn/init_st_xk.do'
req = urllib2.Request(url, None, headers)
urllib2.urlopen(req)
# 补选
# 开始模拟补选
url = 'http://mis.teach.ustc.edu.cn/xkgcinsert.do'
headers['Referer'] = 'http://mis.teach.ustc.edu.cn/init_st_xk_dx.do?queryType=%s&kkdw=&kcmc=&rkjs=' % '4'
# 最后一个匹配返回查询参数
# tag,actionname,xnxq,kcid,kcbjbh,kclb,kcsx,sjpdm,kssjdm,cxck,zylx,gxkfl,xlh,qsz,jzz
xk_data = {
    'cxck': '<cxck>',
    'gxkfl': '<gxkfl>',
    'kcbjbh': '<kcbjbh>',  # 课程班级编号
    'kcid': '<kcid>',  # 课程id，可以从课程列表中取得
    'kclb': '<kclb>',
    'kcsx': '<kcsx>',
    'kssjdm': '<kssjdm>',
    'sjpdm': '<sjpdm>',
    'xlh': '<xlh>',
    'xnxq': '<xnxq>',
    'zylx': '<zylx>'
}
count = 0
retvalue = 'C'
req = urllib2.Request(url, urllib.urlencode(xk_data), headers)
while retvalue[0] != 'D':
    retvalue = urllib2.urlopen(req).read().decode('gbk')
    # 返回值使用前缀表明选课结果，C表示失败，D表示成功
    if retvalue[0] == 'D':
        print u'选课成功，课程编号：' + retvalue
        break
    else:
        print u'\r正在补选: ' + retvalue
    time.sleep(0.5)
