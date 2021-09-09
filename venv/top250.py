# -*- coding: utf-8 -*-
"""
Create Time: 2021/2/19 12:27
Author: charlyq
File: top250.py
"""


import re
import xlwt
import sqlite3
from bs4 import BeautifulSoup
import urllib.request,urllib.error

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #爬取网页
    datalist = getData(baseurl)
    savepath = ".\\doubanTop250.xls"            # 定义保存路径为当前目录
    dbpath = "top250.db"
    #saveData(datalist,savepath)                # 保存到excel表格
    saveData2DB(datalist,dbpath)                # 保存到数据库
    askURL(baseurl)
#影片详情链接
findLink = re.compile(r'<a href="(.*?)">')      #创建正则表达式对象，表示规划（字符串的模式）
#影片图片链接
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)  #re.S让换行符包含在字符中
#影片名字
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#查找概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#查找影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

def getData(baseurl):
    datalist = []
    for i in range(0,10):        # 调用获取页面信息的函数，10次，相当于模拟鼠标点击下一页
        url = baseurl + str(i*25)
        html = askURL(url)       # 保存获取到的网页源码
        soup = BeautifulSoup(html,"html.parser")   # 解析网页数据
        for item in soup.find_all('div',class_="item"):   # 查找符合要求的内容
            #print(item)   # 测试查看电影item全部信息
            data = []   # 保存一部电影的所有信息
            item = str(item)
            # 获取影片详情的链接
            link = re.findall(findLink,item)[0]   # re库用来通过正则表达式查找指定的字符串
            data.append(link)
            # 获取影片图片的链接
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            # 获取影片的名称
            titles = re.findall(findTitle,item)
            if(len(titles) == 2):
                ctitle = titles[0]  #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","")  #去掉/符号
                data.append(otitle)  #添加外国名
            else:
                data.append(titles[0])
                data.append(" ")   #没有外国名则留空
            # 获取影片的评分
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            # 获取影片的评价人数
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)
            # 获取影片的概况
            inq = re.findall(findInq,item)
            if len(inq) !=0:
                inq = inq[0].replace("。","")   #去掉句号
                data.append(inq)
            else:
                data.append(" ")   #留空
            #data.append(inq)
            # 获取影片相关内容
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)   #去掉<br/>
            bd = re.sub('/'," ",bd)   #替换/符号
            data.append(bd.strip())   #去掉前后空格

            datalist.append(data)     #把处理好的一部电影信息放入datalist
            #print(link)
    print(datalist)
    return datalist


#得到指定一个URL的网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }
    #用户代理头部信息，伪装为浏览器
    request = urllib.request.Request(url,headers=head) #利用urllib模块构造http头部
    html = ""
    try:
        response = urllib.request.urlopen(request) #利用前面构造的http头部去请求页面
        html = response.read().decode("utf-8")  #将请求到的页面数据使用utf-8解码后赋值给html
        # print(html)
    except urllib.error.URLError as e:  #捕获错误信息
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html



def saveData(datalist,savepath):
    print("saving....")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)     # 创建workbook对象，也即创建一个工作簿
    sheet = book.add_sheet('Top250',cell_overwrite_ok=True)        # 在工作薄中创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","影片评分","影片评价数","影片概况","影片相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])                                    # 首先填充列名
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)


def saveData2DB(datalist,dbpath):
    print("saving....")
    init_db(dbpath)
    connect = sqlite3.connect(dbpath)
    cur = connect.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into top250 (
            info_link,pic_link,cname,ename,score,rated,instroduction,info)
            values(%s)'''%",".join(data)
        cur.execute(sql)
        connect.commit()
    cur.close()
    connect.close()

def  init_db(dbpath):
    # 创建数据库
    sql = '''
        create table top250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )
    '''
    connect = sqlite3.connect(dbpath)
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()
    connect.close()

if __name__ == "__main__":
    main()
    #init_db(dbpath)
    print("爬取完成！")