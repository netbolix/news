#!/usr/bin/env python3

import os
import json
from datetime import datetime
from flask import Flask,render_template,redirect,url_for,abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://root@localhost/news'
db = SQLAlchemy(app)

path = "/home/shiyanlou/files"


class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',backref='courses')
    content = db.Column(db.Text)

    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


#def listdir(path):
#    FILES = []
#    for file in os.listdir(path):
#        file_path = os.path.join(path,file)
#        if os.path.isdir(file_path):
#            listdir(file_path,FILES)
#        elif os.path.splitext(file_path)[1]=='.json':
#            FILES.append(file_path)
#    return FILES
 


def readfile(file):
    with open(file,'r') as f:
        doc = json.loads(f.read())
    return doc


#@app.route('/')
#def index():
#    titles = []
#    FILES = listdir(path)
##    for file in listdir(path):
#    for file in FILES:
#        doc = readfile(file)
#        titles.append(doc['title'])
#    return render_template('index.html',titles=titles)

@app.route('/')
def index():
    titels = [


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



