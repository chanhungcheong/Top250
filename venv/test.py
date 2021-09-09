# -*- coding: utf-8 -*-
"""
Create Time: 2021/2/19 12:35
Author: charlyq
File: test.py
"""

# from bs4 import BeautifulSoup
# import urllib.request

#获取一个Get请求
# response = urllib.request.urlopen("https://www.ifeng.com")
# print(response.read().decode('utf-8'))

#获取一个Post请求
# html = ""
# print(type(html))

# file = open("./baidu.html","rb")
# html = file.read()
# bs = BeautifulSoup(html,"html.parser")  #解析文档

# print(bs.title)
# print(bs.a)
# print(bs.head)

# print(type(bs.head))

#1.Tag 标签及其内容，拿到它所找到的第一个内容

# print(bs.title.string)

#2.NavigableString 标签里的内容（字符串），还有标签里的属性

#print(bs.a.attrs)

#3.BeautifulSoup 表示整个文档

#4.Comment 是一个特殊的NavigableString，输出的内容不包含注释符号

#文档的遍历，更多内容使用搜索文档
# print(bs.head.comment)

#文档的搜索
#1.find_all()
#字符串过滤：会查找与字符串完全匹配的内容
#t_list = bs.find_all("a")

#2.正则表达式搜索：使用search()方法来匹配内容
# import re
#t_list = bs.find_all(re.compile("a"))

#3.方法：传入一个函数，按函数要求进行搜索

#CSS选择器
#t_list = bs.select('title') #通过标签来查找
#t_list = bs.select(".mnav") #通过类名来查找
#t_list = bs.select('#u1')  #通过id来查找
#t_list = bs.select("a[class='bri']")  #通过性能来查找
#t_list = bs.select("head > title")  #通过子标签来查找
# t_list =  bs.select(".mnav ~ .bri")  #通过兄弟标签来查找
# print(t_list[0].get_text())

#sub：替换
# print(re.sub("a","A","abcdsefdfasf")) #在最后面参数abcdsefdfasf中找到a然后用A进行替换

# import xlwt

# workbook = xlwt.Workbook(encoding="utf-8")     # 创建workbook对象，也即创建一个工作簿
# worksheet = workbook.add_sheet('sheet1')       # 在工作薄中创建工作表
# worksheet.write(0,0,'hello')                   # 写入数据，第一个参数是“行”，第二个参数是“列”，第三个参数是写入的内容
# workbook.save('test.xls')                      # 保存工作簿

# workbook = xlwt.Workbook(encoding="utf-8")     # 创建workbook对象，也即创建一个工作簿
# worksheet = workbook.add_sheet('sheet1')       # 在工作薄中创建工作表
# for i in range(0,9):                           # 打印九九乘法表并写入excel表格中
#     for j in range(0,i+1):
#         worksheet.write(i,j,"%d * %d = %d"%(i+1,j+1,(i+1)*(j+1)))
# workbook.save('test1.xls')

# import sqlite3
# 
# connect = sqlite3.connect("testsqlite.db")
# 
# print("成功打开数据库!")
# 
# c = connect.cursor()    # 获取游标
# 
# sql = '''
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char(50),
#         salary real);
# '''
# 
# c.execute(sql)          # 执行sql语句
# connect.commit()        # 提交数据库操作
# connect.close()         # 关闭数据库连接
# 
# print("成功建表！")

from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/index")
def index():
    return ""

if __name__ == '__main__':
    app.run()