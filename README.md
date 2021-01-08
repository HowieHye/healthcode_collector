# HEALTHY CODE COLLECTOR

Modify from [xrandx/tiny-tools](https://github.com/xrandx/tiny-tools)

快速收集班级同学健康码

## 食用方法

### 修改文件

1. `web.py`

``` diff
- application.config['MAIL_SERVER'] = 'smtp.qq.com' # 邮件服务地址
- application.config['MAIL_PORT'] = '465'
- application.config['MAIL_USERNAME'] = ''  # 邮箱地址
- application.config['MAIL_PASSWORD'] = ''  # 邮箱密码/授权码


def db_execute(query):
    db = pymysql.connect(
-         host="localhost",  # 数据库主机地址
-         user="admin",  # 数据库用户名
-         port=3306,
-         passwd="123456",  # 数据库密码
-         database="health_code"  # 数据库名
    )
    cur = db.cursor()
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    db.close()
    return res


def database_start():
    global name_dict
-     result = db_execute("SELECT name, id, dept FROM 17dx1;")
    for i in result:
        name = str(i[0])
        name_dict[name] = (str(i[1]), str(i[2]))


def send_email():
    compressed_file = datetime.date.today().strftime("%m-%d") + '.zip'
    with ZipFile(PROGRAM_DIR + "static/" + compressed_file, "w") as myzip:
        file_array = listdir(PROGRAM_DIR + "static/uploads")
        chdir(PROGRAM_DIR + "static/uploads")
        for file in file_array:
            myzip.write(file)
    chdir(PROGRAM_DIR + "static")
-     email_subject = datetime.date.today().strftime("%m月%d日") + "17电信1班 行程轨迹"
-     msg = Message(email_subject, sender='howiehye@qq.com',
                  recipients=['howiehye@163.com'])
    msg.body = email_subject
    SendFileName = PROGRAM_DIR+"static/"+compressed_file
    with application.open_resource(SendFileName) as fp:
        msg.attach(SendFileName, 'application/zip', fp.read())
    thr = threading.Thread(target=send_async_email, args=[application, msg])
    thr.start()
```

2. `templates/index.html`

``` diff
-   <title>17电信1班行程轨迹收集</title>

-           <h1 style="text-align: center">17电信1班行程轨迹收集</h1>

-           class="icp-icon" src="/static/images/icp.png" alt="ICP"><span>苏ICP备20045438号-1</span></a>
```

3. `templates/admin.html`

``` diff
-   <title>17电信1班 行程轨迹管理</title>

-           <h1 style="text-align: center">17电信1班 行程轨迹管理</h1>

-           class="icp-icon" src="/static/images/icp.png" alt="ICP"><span>苏ICP备20045438号-1</span></a>
```

### 使用宝塔面板部署

软件商店 -> Python项目管理器 -> 添加项目 -> 选择项目目录\框架为`flask`\启动方式`uwsgi`

## 鸣谢

- [xrandx](https://github.com/xrandx)
- [Daisy-1999](https://github.com/Daisy-1999)

## LICENSE

[GPL v3.0](./LICENSE)
