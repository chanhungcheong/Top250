# -*- coding: utf-8 -*-
"""
Create Time: 2021/2/20 14:59
Author: charlyq
File: app.py
"""
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/index")
def index():
    time = datetime.date.today()
    name = ["zhang", "chen", "zhao"]
    return render_template("index.html", var=time, list=name)


if __name__ == '__main__':
    app.run()
