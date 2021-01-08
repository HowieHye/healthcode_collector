# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, jsonify, redirect, request, url_for, send_from_directory, abort, \
    json, Blueprint
from flask_mail import Mail, Message
from os.path import split, realpath, join, getsize, exists
import pymysql
from os import listdir, rename, chdir, remove, getcwd
from zipfile import ZipFile
import datetime
from pypinyin import lazy_pinyin
from werkzeug.utils import secure_filename
import threading

application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
application.config['SQLALCHEMY_POOL_RECYCLE'] = 400
application.config['JSON_AS_ASCII'] = False
application.config['MAIL_SERVER'] = 'smtp.qq.com'
application.config['MAIL_PORT'] = '465'
application.config['MAIL_USERNAME'] = ''
application.config['MAIL_PASSWORD'] = ''
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
application.jinja_env.block_start_string = '(%'  # 修改块开始符号
application.jinja_env.block_end_string = '%)'  # 修改块结束符号
application.jinja_env.variable_start_string = '((_'  # 修改变量开始符号
application.jinja_env.variable_end_string = '_))'  # 修改变量结束符号
application.jinja_env.comment_start_string = '(#'  # 修改注释开始符号
application.jinja_env.comment_end_string = '#)'  # 修改注释结束符号
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'tif', 'zip'}

PROGRAM_DIR = split(realpath(__file__))[0] + "/"

mail = Mail(application)


def db_execute(query):
    db = pymysql.connect(
        host="localhost",  # 数据库主机地址
        user="admin",  # 数据库用户名
        port=3306,
        passwd="123456",  # 数据库密码
        database="health_code"  # 数据库名
    )
    cur = db.cursor()
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    db.close()
    return res


name_dict = {}


def database_start():
    global name_dict
    result = db_execute("SELECT name, id, dept FROM 17dx1;")
    for i in result:
        name = str(i[0])
        name_dict[name] = (str(i[1]), str(i[2]))


@application.route('/download')
def download_file():
    compressed_file = datetime.date.today().strftime("%m-%d") + '.zip'
    if exists(PROGRAM_DIR + "static/" + compressed_file):
        remove(PROGRAM_DIR + "static/" + compressed_file)
    with ZipFile(PROGRAM_DIR + "static/" + compressed_file, "w") as myzip:
        file_array = listdir(PROGRAM_DIR + "static/uploads")
        chdir(PROGRAM_DIR + "static/uploads")
        for file in file_array:
            myzip.write(file)
    addr = "/static/" + compressed_file
    print(jsonify(addr))
    return jsonify(addr)


@application.route('/delete')
def delete_file():
    file_array = listdir(PROGRAM_DIR + "static/uploads")
    chdir(PROGRAM_DIR + "static/uploads")
    for file in file_array:
        # print(file)
        remove(file)
    file_array = listdir(PROGRAM_DIR + "static/uploads")
    return jsonify(file_array)


@application.route('/send_email')
def email_main():
    send_email()
    print("email send!")
    return "Sent"


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email():
    compressed_file = datetime.date.today().strftime("%m-%d") + '.zip'
    with ZipFile(PROGRAM_DIR + "static/" + compressed_file, "w") as myzip:
        file_array = listdir(PROGRAM_DIR + "static/uploads")
        chdir(PROGRAM_DIR + "static/uploads")
        for file in file_array:
            myzip.write(file)
    chdir(PROGRAM_DIR + "static")
    email_subject = datetime.date.today().strftime("%m月%d日") + "17电信1班 行程轨迹"
    msg = Message(email_subject, sender='howiehye@qq.com',
                  recipients=['howiehye@163.com'])
    msg.body = email_subject
    SendFileName = PROGRAM_DIR+"static/"+compressed_file
    with application.open_resource(SendFileName) as fp:
        msg.attach(SendFileName, 'application/zip', fp.read())
    thr = threading.Thread(target=send_async_email, args=[application, msg])
    thr.start()
    # return jsonify(message)


@application.route('/forget')
def forget():
    global name_dict
    database_start()
    file_array = listdir(PROGRAM_DIR + "static/uploads")
    forget_list = list()
    for zw_name in name_dict.keys():
        flag = False
        for file_name in file_array:
            if zw_name in file_name:
                flag = True
                break
        if not flag:
            forget_list.append({"forget_name": zw_name})
    return jsonify(forget_list)


@application.route('/')
def index():
    database_start()
    return render_template('index.html')


@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        json_data = request.form["data"]
        name = json.loads(json_data)["name"]
        filename = secure_filename(f.filename)
        idx = filename.rindex(".")
        filename = name + filename[idx:]
        upload_path = join(PROGRAM_DIR, "static/uploads/", filename)
        f.save(upload_path)
        return jsonify("static/uploads/" + filename)


@application.route('/view')
def view_pictures():
    pic_list = list()
    pic_dir = join(PROGRAM_DIR, "static/uploads")
    pic_names = listdir(pic_dir)
    for pic_name in pic_names:
        pic_list.append(
            {'img_name': pic_name, 'img_path': '/static/uploads/' + pic_name})
    return jsonify(pic_list)


@application.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    application.run()
