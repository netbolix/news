#!/usr/bin/env python3

import os
import json
from flask import Flask,render_template,redirect,url_for,abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

path = "/home/shiyanlou/files"

def listdir(path):
    FILES = []
    for file in os.listdir(path):
        file_path = os.path.join(path,file)
        if os.path.isdir(file_path):
            listdir(file_path,FILES)
        elif os.path.splitext(file_path)[1]=='.json':
            FILES.append(file_path)
    return FILES

def readfile(file):
    with open(file,'r') as f:
        doc = json.loads(f.read())
    return doc


@app.route('/')
def index():
    titles = []
    FILES = listdir(path)
#    for file in listdir(path):
    for file in FILES:
        doc = readfile(file)
        titles.append(doc['title'])
    return render_template('index.html',titles=titles)



@app.route('/files/<filename>')
def file(filename):
        file_new = filename + '.json'
        file_path = os.path.join(path,file_new)
        if os.path.exists(file_path):
           doc = readfile(file_path)
           return render_template('file.html',doc=doc)
        else:
            abort(404)
#           return redirect(url_for(not_found))



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404



