# coding: UTF-

import requests
import sys
import time
import json
import os
from pyquery import PyQuery as pq
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mail(msg):
    my_sender = 'chenxiaozong@szbailiao.com'  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
    my_user = 'hk-alian@qq.com'  # 收件人邮箱账号，为了后面易于维护，所以写成了变量
    try:
        msg = MIMEText(msg, 'plain', 'utf-8')
        msg['From'] = formataddr(["来自新闻抓取 Python", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["粽子", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "邮件提醒"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.ym.163.com", 994)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, "xiaozong.")  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 这句是关闭连接的意思
    except Exception as e:  # 如果try中的语句没有执行，则会执行下面的ret=False
        mail(str(e))


# 上次抓取的最大时间
last_max_time = {
    '1': ''
    , '2': ''
    , '3': ''
    , '4': ''
    , '5': ''
    , '6': ''
    , '7': ''
    , '8': ''
    , '9': ''
    , '10': ''
    , '11': ''
    , '12': ''
    , '13': ''
    , '14': ''
}
# 抓取的次数
times = 0
# 新闻上传地址
upload_url = 'http://news.alian.me/upload.html'
# 新闻资源上传后的访问地址
new_img_url = ''
# 频道id
channle_num = {
    '1': '头条'
    , '2': '新闻'
    , '3': '财经'
    , '4': '体育'
    , '5': '娱乐'
    , '6': '军事'
    , '7': '教育'
    , '8': '科技'
    , '9': 'NBA'
    , '10': '股票'
    , '11': '星座'
    , '12': '女性'
    , '13': '健康'
    , '14': '育儿'
}
# 对应id的抓取链接
news_urls = {
    # 新闻
    '2': 'http://temp.163.com/special/00804KVA/cm_yaowen.js?callback=data_callback'
    # 军事
    , '6': 'http://temp.163.com/special/00804KVA/cm_war.js?callback=data_callback'
    # 女性
    , '12': 'http://lady.163.com/special/00264OOD/data_nd_sense.js?callback=data_callback'
    # 科技
    , '8': 'http://tech.163.com/special/00097UHL/tech_datalist.js?callback=data_callback'
    # 股票
    , '10': 'http://money.163.com/special/002557S6/newsdata_gp_index.js?callback=data_callback'
    # 娱乐
    , '5': 'http://ent.163.com/special/000380VU/newsdata_index.js?callback=data_callback'

    # 头条
    , '1': 'http://news.163.com/special/yaowen_channel_api/?callback=channel_callback&date=0120'
    # 财经
    , '3': 'http://money.163.com/special/002557S5/newsdata_idx_index.js?callback=data_callback'
    # 体育
    , '4': 'http://sports.163.com/special/000587PR/newsdata_n_index.js?callback=data_callback'
    # 教育
    , '7': 'http://edu.163.com/special/002987KB/newsdata_edu_hot.js?callback=data_callback'
    # NBA
    , '9': 'http://sports.163.com/special/000587PK/newsdata_nba_index_02.js?callback=data_callback'
    # 星座
    , '11': ''
    # 健康
    , '13': ''
    # 育儿
    , '14': 'http://baby.163.com/special/003687OS/newsdata_hot.js?callback=data_callback'

}
# 睡眠时间
sleep_time = 600


def post(url, d):
    r = requests.post(url, d)
    del d
    try:
        return r.json()
    except Exception as e:
        log("请求返回错误 地址" + url)
        log("请求返回错误 数据" + str(r))


def get(url):
    try:
        r = requests.get(url)
        return r.text
    except Exception as e:
        return False

# 处理新闻的内容
def handleNewsContent(content):
    # 正则不必要的 DIV
    # div = r'<div.*</div>'
    # return re.sub(div,'',content)
    content = pq(content)
    content.find('.ep-editor').remove()
    content.find('iframe').remove()
    content.find('.icon').remove()
    # 移除视频
    content.find('object').remove()
    # 让所有 A 链接失效
    content.find('a').attr('href', 'javascript:void(0);')
    content = str(content.html())
    # 替换 &amp; 为 & 防止图片替换失败
    return content.replace('&amp;', '&')


# 获取新闻中的图片
def getNewsImage(content):
    # 缓存图片地址
    tmp = []
    # 取出图片
    content = pq(content).find('img')
    # 遍历图片的链接
    for i in content.items():
        tmp.append(i.attr('src'))
    return tmp


# 上传新闻图片链接到 七牛
def uploadImg(list):
    if len(list) == 0:
        return True
    # 缓存上传后的地址
    cache = {}
    global url
    url = ''
    for item in list:
        post_data = {
            'type': 'upload',
            'url': item
        }
        # 上传文件
        rs = post(upload_url, post_data)
        if rs['status'] == True:
            # 上传成功
            cache[item] = rs['key']
            url = rs['url']
        else:
            # 上传失败
            cache[item] = False
    return cache, url


def deleteImg(list):
    post(upload_url, {'type': 'delete_img', 'list': json.dumps(list)})


# 替换文章内容的 图片地址
def replaceImg(content, imgList, Imgurl):
    for k in imgList.keys():
        if k is None or imgList[k] is None:
            continue
        content = content.replace(k, Imgurl + str(imgList[k]))
    return content


# 记录日志文件
def log(msg):
    f = open('get_163_news.log', 'w')
    f.write(msg + '\n')
    f.close()


# 处理新闻
def handleNews(news):
    # 首先检查新闻是否可以上传
    check_data = {'type': 'check', 'title': news['title']}
    check_rs = post(upload_url, check_data)
    # 判断返回结果是否可以上传
    if check_rs['status']:
        # 获取新闻内容
        
        html = pq(get(news['docurl']))
        # 获取新闻的内容
        content = html('.post_text').html()
        # 新闻内容处理
        content = handleNewsContent(content)
        # 获取内容中的图片
        img_list = getNewsImage(content)
        if len(img_list) == 0:
            #print '跳过新闻: ' + news['title']
            #return
            img_list = news['imgurl']
        # 七牛云上传
        upload_list, Imgurl = uploadImg()
        # 第一张图片上传失败就不要再继续了
        if not upload_list.values()[0]:
            print '跳过新闻: ' + news['title']
            return
        # 把原内容的图片url 替换成 上传后的url
        content = replaceImg(content, upload_list, Imgurl)

        # 上传到服务器
        send_data = {
            'type': 'upload_news',
            'channel': channel,
            'title': news['title'],
            'content': content,
            'from': '网易新闻',
            'news_time': news['time'],
            'first_pic': Imgurl + upload_list.values()[0],
            'img_list': json.dumps(upload_list.values())
        }
        del Imgurl
        rs = post(upload_url, send_data)
        if rs['status']:
            print '[' + channle_num[channel] + ']' + str(
                time.strftime('%m-%d %H:%M', time.localtime(time.time()))) + ' 添加新闻: ' + news['title']
        else:
            deleteImg(upload_list.values())
    else:
        print '跳过新闻: ' + news['title']
    # 不要太快了
    time.sleep(2)


# 程序入口
if __name__ == '__main__':
    # 解决因为编码问题报问错题
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #if os.path.exists('.idea') == False:
    #    upload_url = 'http://news.szbailiao.com/upload.html'
    while True:
        for channel in news_urls.keys():
            print '*' * 20 + channle_num[channel] + '*' * 20
            # 163 的 json
            html = get(news_urls[channel])
            if html == False :
                continue
            # 移除不必要的函数体
            html = json.loads(html.replace('data_callback(', '')[:-1])
            # 遍历新闻条数
            for x in html:
                # 如果当前新闻的类型是图集 不收集
                if x['newstype'] != 'article':
                    continue
                # 转化新闻里面的时间为 时间戳
                try:
                    tmp_time = time.mktime(time.strptime(x['time'], '%m/%d/%Y %H:%M:%S'))
                except Exception:
                    log('解析日期错误: ' + x['time'])
                    tmp_time = last_max_time
                # 第一次 或者 此新闻的更新时间比上次抓取的最大时间大
                if times == 0 or last_max_time[channel] < tmp_time:
                    # 这里的判断是为了解决第一次抓取 最大时间是不正确的
                    if last_max_time[channel] == '' or last_max_time[channel] < tmp_time:
                        last_max_time[channel] = tmp_time
                    # 处理新闻
                    handleNews(x)
        # 记录抓取次数
        times = times + 1
        print '等待第 ' + str(times + 1) + '次抓取'
        # 睡眠
        cur_hours = time.strftime('%H', time.localtime(time.time()))
        if cur_hours in ['24', '00', '01', '02', '03', '04', '05', '06', '07', '08']:
            # 一个小时抓一次
            sleep_time = 3600
        else:
            # 10分钟抓一次
            sleep_time = 600
        time.sleep(sleep_time)
