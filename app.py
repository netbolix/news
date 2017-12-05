#!/usr/bin/env python3

import os
import json
from datetime import datetime
from flask import Flask,render_template,redirect,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

app = Flask(__name__)
#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://root@localhost/news'
db = SQLAlchemy(app)

#client = MongoClient('127.0.0.1',27017)
mongo = MongoClient('127.0.0.1',27017).shiyanlou
#mongo =client.shiyanlou

#path = "/home/shiyanlou/files"


class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
#    category = db.relationship('Category',uselist=False,backref='file')
    category = db.relationship('Category',uselist=False)
    content = db.Column(db.Text)

    def __init__(self,title,created_time,category,content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def add_tag(self,tag_name):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            if tag_name not in tags:
                tags_append(tag_name)
            mongo.files.update_one({'file_id': self.id},{'$set':{'tags': tags}})
        else:
            tags = [tag_name]
            mongo.files.insert_one({'files_id': self.id,'tags': tags})
        return tags


    def remove_tag(self,tag_name):
        file_time = mongo.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            try:
                tags.remove(tag_name)
                new_tags = tags
            except ValueError:
                return tags
            mongo.files.update_one({'file_id': self.id},{'$set':{'tags': tags}})
            return new_tags
        return []

    @property
    def tags(self):
        file_item = mongo.files.find_one({'file_id': self.id})
        if file_item:
            print(file_item)
            return file_item['tags']
        else:
            return []

    def __repr__(self):
        return '<File %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    file = db.relationship('File')

    def __init__(self,name):
        self.name = name

#    def __repr__(self):
#        return '<Category %r>' % self.name

def insert_data():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java',datetime.utcnow(),java,'File Content - Java is cool!')
    file2 = File('Hello python',datetime.utcnow(),python,'File Content - python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()
    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')

@app.route('/')
def index():
    return render_template('index.html',files=File.query.all())

@app.route('/files/<int:file_id>')
def file(file_id):
    file_item = File.query.get_or_404(file_id)
    return render_template('file.html',file_item=file_item)


#def listdir(path):
#    FILES = []
#    for file in os.listdir(path):
#        file_path = os.path.join(path,file)
#        if os.path.isdir(file_path):
#            listdir(file_path,FILES)
#        elif os.path.splitext(file_path)[1]=='.json':
#            FILES.append(file_path)
#    return FILES
 


#def readfile(file):
#    with open(file,'r') as f:
#        doc = json.loads(f.read())
#    return doc


#@app.route('/')
#def index():
#    titles = []
#    FILES = listdir(path)
##    for file in listdir(path):
#    for file in FILES:
#        doc = readfile(file)
#        titles.append(doc['title'])
#    return render_template('index.html',titles=titles)


#@app.route('/files/<filename>')
#def file(filename):
#        file_new = filename + '.json'
#        file_path = os.path.join(path,file_new)
#        if os.path.exists(file_path):
#           doc = readfile(file_path)
#           return render_template('file.html',doc=doc)
#        else:
#            abort(404)
#           return redirect(url_for(not_found))



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


if __name__ == '__main__':
    app.run()
