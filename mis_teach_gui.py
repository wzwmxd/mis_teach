# -*- coding: utf-8 -*-
import urllib2, urllib, cookielib, re
from Tkinter import *
import ttk

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US, en;q = 0.5',
    'Connection': 'keep-alive',
    'Cookie': '_gscu_1103646635=69155042d0dour98; _gscs_1103646635=69155042wyvvcb98|pv:1; _ga=GA1.3.234722701.1469155052; _gat=1',
    'Host': 'mis.teach.ustc.edu.cn',
    'User-Agent': 'Mozilla/5.0(X11;Ubuntu;Linux x86_64;rv:47.0) Gecko/20100101 Firefox/47.0'
}

logined = False


def update(show_view, course_type):
    # 开始选课
    url = 'http://mis.teach.ustc.edu.cn/init_st_xk_dx.do'
    headers['Referer'] = 'http://mis.teach.ustc.edu.cn/init_st_xk_dx.do'
    data = {
        'kcmc': '',
        'kkdw': '',
        'qr_queryType': 'null',
        'queryType': course_type,
        'rkjs': '',
        'seldwdm': 'null',
        'selkkdw': '',
        'seyxn': '2016',  # 学年
        'seyxq': '1',  # 学期
        'sjpdmlist': '',
        'xnxq': '20161'  # 学期 + 学年
    }
    req = urllib2.Request(url, urllib.urlencode(data), headers)
    response = urllib2.urlopen(req)
    course_html = response.read().decode('GBK').encode('utf-8')
    course_list = get_course(course_html)

    x = tree_course.get_children()
    for item in x: tree_course.delete(item)
    for i, elem in enumerate(course_list):
        item = []
        for j in range(len(elem)):
            # 去除转义字符和html标签
            item.append(elem[j].replace('&nbsp', '').replace('<br>', ' '))  # .decode('utf-8').encode('gb18030'))
        show_view.insert('', i, values=tuple(item))
    e_code.selection_clear()
    if len(course_list) == 0:
        code.set("Nothing")


def get_cookie(checklabel):
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
    response.read()
    # 尚不清楚date的用处，但是可以一直使用如下值
    date = '1469242601259'
    url = 'http://mis.teach.ustc.edu.cn/randomImage.do?date=%%27%s%%27' % date
    headers['Accept'] = '*/*'
    headers['Referer'] = 'http://mis.teach.ustc.edu.cn/userinit.do'
    data = {'date': date}
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    compressedData = response.read()
    # f = open('random_img_file.jpg', 'w')  # 保存验证码图片的路径，最近的教务系统取消了验证码
    # print >> f, compressedData
    # f.close()
    # Image.open('random_img_file.jpg').save('random_img_file.gif')
    # img = PhotoImage(file='random_img_file.gif')
    # checklabel['image'] = img


def login(username='', passwd='', checkcode=''):
    # 提交用户名，密码和验证码，模拟登录
    url = 'http://mis.teach.ustc.edu.cn/login.do'
    data = {
        'check': checkcode,
        'passWord': passwd,
        'userCode': username,
        'userbz': 's'
    }
    # data['check'] = ''  # raw_input('Please input check_code:')
    # data['userCode'] = ''  # raw_input('Username: ')
    # data['passWord'] = ''  # raw_input('Password: ')
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data, headers)
    urllib2.urlopen(req)
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


def get_course(course_html):
    # print >> open('index.html', 'w'), course_html
    course1 = r'<td.+?>[\r\n\t ]*' + \
              r'<a.+?>[\r\n\t ]*' + \
              r'<font.+?>(.+?)</font>[\r\n\t ]*' + \
              r'</a>[\r\n\t ]*.+?</td>[\r\n\t ]*'
    course2 = r'<td(.+?)>[\r\n\t ]*.+?</td>[\r\n\t ]*'
    course_exp1 = r'<td.+?>[\r\n\t ]*' + \
                  r'(\d+?)[\r\n\t ]*</td>[\r\n\t ]*' + \
                  r'<td.+?>[\r\n\t ]*([\d\w]+?)[\r\n\t ]*</td>[\r\n\t ]*' + \
                  r'<td.+?>[\r\n\t ]*<a.+?kcid=(.+?)&bjbh=.+?>[\r\n\t ]*' + \
                  r'<font.+?>(.+?)</font>[\r\n\t ]*' + \
                  r'</a>[\r\n\t ]*</td>[\r\n\t ]*'
    course_exp2 = r'<td.+?>(.+?)</td>[\r\n\t ]*' + \
                  r'<td.+?>(.+?)</td>[\r\n\t ]*' + \
                  r'<td.+?>(.+?)</td>[\r\n\t ]*' + \
                  r'<td.+?>(.+?)</td>[\r\n\t ]*' + \
                  r'<td.+?>[\r\n\t ]*([\d/]+?)[\r\n\t ]*</td>[\r\n\t ]*' + \
                  r'<td.+?>[\r\n\t ]*(.+?)[\r\n\t ]*</td>[\r\n\t ]*' + \
                  r'<td.+?>[\r\n\t ]*.+?[\r\n\t ]*' + \
                  r'<input.+?[\r\n\t ]*.+?[\r\n\t ]*' + \
                  r'onclick="return querykc\((.+?)\);"/>'
    # 最后一个匹配返回查询参数
    # tag,actionname,xnxq,kcid,kcbjbh,kclb,kcsx,sjpdm,kssjdm,cxck,zylx,gxkfl,xlh,qsz,jzz
    course_reg1 = re.compile(course_exp1 + course1 + course_exp2)
    course_reg2 = re.compile(course_exp1 + course2 + course_exp2)
    retList = course_reg1.findall(course_html) + course_reg2.findall(course_html)
    retList.sort(key=lambda x: int(x[0]))
    return retList


def query_course():
    course_type_dict = {
        u'计划内课程': '1',
        u'自由选修': '2',
        u'公选课': '4',
        u'体育选课': '5',
        u'英语选课': '6'
    }
    global logined
    if logined == False:
        login(Username.get(), Password.get(), '')
        logined = True
    update(tree_course, course_type_dict[var_type.get()])


def get_type(*args):
    pass


def onDBClick(event):
    item = tree_course.selection()[0]
    e_code.selection_clear()
    info_code = tree_course.item(item, "values")
    code.set(info_code[3] + '@' + info_code[4] + '@' + info_code[11])


def gen_code():
    source = open('gen_templete.py').read().decode('utf-8')
    info = code.get().split('@')[-1]
    info = info.split(',')
    xk_data = {
        'checkcode': '\'' + Checkcode.get() + '\'',
        'passwd': '\'' + Password.get() + '\'',
        'username': '\'' + Username.get() + '\'',
        'cxck': info[10],
        'gxkfl': info[12],
        'kcbjbh': info[4],  # 课程班级编号
        'kcid': info[3],  # 课程id，可以从课程列表中取得
        'kclb': info[5],
        'kcsx': info[6],
        'kssjdm': info[9],
        'sjpdm': info[7] + ',' + info[8],
        'xlh': info[13],
        'xnxq': info[2],
        'zylx': '\'01\''  # info[11]  # 这一项是什么意思？
    }
    for i in xk_data:
        source = source.replace('\'<%s>\'' % i, '%s' % xk_data[i])
    print >> open('gencode.py', 'w'), source.encode('utf-8')
    e_code.selection_clear()
    code.set("生成刷课脚本成功！")


logined = False
root = Tk()
root.title("mis_teach")
root.geometry('1000x300')
f_info = Frame(root)
# 用户名
l_username = Label(f_info, text='Username')
l_username.pack(side=LEFT)
Username = StringVar()
e_username = Entry(f_info, textvariable=Username)
e_username.pack(side=LEFT)
# 密码
l_password = Label(f_info, text='Password')
l_password.pack(side=LEFT)
Password = StringVar()
e_password = Entry(f_info, textvariable=Password, show='*')
e_password.pack(side=LEFT)
# 验证码
l_checkcode = Label(f_info, text='[check code]', image=None)
l_checkcode.pack(side=LEFT)
get_cookie(l_checkcode)  # 获得cookie并显示验证码
Checkcode = StringVar()
e_checkcode = Entry(f_info, textvariable=Checkcode)
e_checkcode.pack(side=LEFT)
# 选课类型
var_type = StringVar()
c_type = ttk.Combobox(f_info, textvariable=var_type)
c_type['values'] = (u'计划内课程', u'自由选修', u'公选课', u'体育选课', u'英语选课')
c_type['state'] = 'readonly'
c_type.current(2)
c_type.bind("<<ComboboxSelected>>", get_type)
c_type.pack(side=LEFT)
Button(f_info, text='Query', command=query_course).pack(side=LEFT)
Button(f_info, text='Generate', command=gen_code).pack(side=LEFT)
f_info.pack(side=TOP)

f_course = Frame(root)
tree_course = ttk.Treeview(f_course, show='headings',
                           columns=('no', 'kcbjbh', 'kcid', 'kcmc', 'teacher',
                                    'depart', 'tap', 'grade', 'week',
                                    'people', 'prop'))
tree_course.column('no', width=50, anchor='center')
tree_course.heading('no', text=u'序号')
tree_course.column('kcbjbh', width=80, anchor='center')
tree_course.heading('kcbjbh', text=u'课堂号')
tree_course.column('kcid', width=50, anchor='center')
tree_course.heading('kcid', text=u'课程号')
tree_course.column('kcmc', width=140, anchor='center')
tree_course.heading('kcmc', text=u'课程名称')
tree_course.column('teacher', width=50, anchor='center')
tree_course.heading('teacher', text=u'教师')
tree_course.column('depart', width=140, anchor='center')
tree_course.heading('depart', text=u'开课单位')
tree_course.column('tap', width=160, anchor='center')
tree_course.heading('tap', text=u'上课地点、时间')
tree_course.column('grade', width=50, anchor='center')
tree_course.heading('grade', text=u'学分')
tree_course.column('week', width=70, anchor='center')
tree_course.heading('week', text=u'起止周')
tree_course.column('people', width=120, anchor='center')
tree_course.heading('people', text=u'限选/已选/选中(人)')
tree_course.column('prop', width=60, anchor='center')
tree_course.heading('prop', text=u'课程属性')

tree_course.bind("<Double-1>", onDBClick)
tree_course.pack(side=TOP)
vbar = ttk.Scrollbar(f_course, orient=VERTICAL, command=tree_course.yview)
tree_course.configure(yscrollcommand=vbar.set)
tree_course.grid(row=0, column=0, sticky=NSEW)
vbar.grid(row=0, column=1, sticky=NS)
f_course.pack(side=TOP)

f_code = Frame(root, width=500)
code = StringVar()
e_code = Entry(f_code, width=400, textvariable=code)
e_code.pack(side=LEFT)
f_code.pack(side=TOP)
root.mainloop()
