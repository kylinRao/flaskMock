#coding:utf-8

# curl -O https://pypi.python.org/packages/source/p/pip/pip-1.2.1.tar.gz
# tar xvfz pip-1.2.1.tar.gz
# cd pip-1.2.1
# python setup.py install

import os
import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object("appConfig.DevelopmentConfig")

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

def init_db():
    with app.app_context():
        db = get_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text ,id from entries order by id desc')
    entries = [dict(title=row[0], text=row[1] ,id = row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        flash('please login first!!')
        return redirect(url_for('login'))
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
@app.route('/addcomment', methods=['POST'])
def add_comment():
    print request.form
    g.db.execute('insert into comments ( "comment" ) values ( "{postcomment}" )'.format(postcomment=request.form['commentAdd']))
    g.db.commit()
    flash('New comment added!!')
    return redirect(url_for('pdf'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))
@app.route('/delete/<post_id>/',methods=['GET', 'POST'])
def delete(post_id):
    print post_id
    if not session.get('logged_in'):
        flash('please login first!!')
        return redirect(url_for('login'))
    g.db.execute('delete from entries where id= {post_id}'.format(post_id = post_id))
    g.db.commit()
    flash('delete content success!')
    return redirect(url_for('show_entries'))
@app.route('/contentDetail/<post_id>/',methods=['GET', 'POST'])
def contentDetail(post_id):
    print post_id
    if not session.get('logged_in'):
        flash('please login first!!')
        return redirect(url_for('login'))
    cur = g.db.execute('select title, text ,id from entries where id = {post_id}'.format(post_id=post_id))
    entries = [dict(title=row[0], text=row[1] ,id = row[2]) for row in cur.fetchall()]
    return render_template('contentDetail.html',entries=entries)
@app.route('/showPdf',methods=['GET', 'POST'])
def showPdf():
    return render_template('showPdf.html')
@app.route('/showPdf2',methods=['GET', 'POST'])
def showPdf2():
    return render_template('showPdf2.html')
@app.route('/pdf',methods=['GET', 'POST'])
def pdf():
    cur = g.db.execute('select comment,id from comments  ORDER by id DESC ')
    entries = [dict(comment=row[0],id =row[1]) for row in cur.fetchall()]
    print entries
    filesList = []
    for file in os.listdir("static/pdf"):
        filesList.append({"path":"static/pdf/"+file,"fileName":file})
    return render_template('pdf.html',entries=entries,filesList=filesList)

@app.route('/commentDelete/<post_id>/',methods=['GET', 'POST'])
def commentDelete(post_id):
    print post_id
    g.db.execute('delete from comments where id= {post_id}'.format(post_id = post_id))
    g.db.commit()
    flash('delete content success!')
    return redirect(url_for('pdf'))
@app.route('/add_comment_json',methods=['POST'])
def add_comment_json():
    print request.form
    g.db.execute('insert into comments ( "comment" ) values ( "{postcomment}" )'.format(postcomment=request.form['commentAdd']))
    g.db.commit()
    cur = g.db.execute('select comment,id from comments ORDER by id desc limit 1')
    data = [dict(comment=row[0],id =row[1]) for row in cur.fetchall()]
    print data

    return json.dumps(data)
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/pdf',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')

if __name__ == '__main__':
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')




    app.run(host='0.0.0.0')
