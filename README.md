# flask-demo

&emsp;&emsp;flask入门样例，从[官方教程](http://docs.jinkan.org/docs/flask/tutorial/index.html)开始练起，并根据实际开发需要，
合理的拆分各个模块，便于代码的维护。
昨天偶然间找到[cookiecutter-flask](https://github.com/sloria/cookiecutter-flask)这款工具，于是乎试用了一下，发现十分惊艳，
而且[cookiecutter](https://github.com/audreyr/cookiecutter)可以说是SaaS工程构建的福音，通过模板的方式设计工程结构。
于是乎，我试用了一下，并从中借鉴了许多，惭愧惭愧。       

这里还有一篇文章，大家可以借鉴下：[Flask 大规模实践](http://liuliqiang.info/post/121/)

## 一. 目录结构：
   
   - *blueprints*     
   &emsp;&emsp;将业务逻辑分给为多个blueprint（app），以便功能复用和维护
   - *models*     
   &emsp;&emsp;数据库建模文件夹，包括主动建模和被动探测两种方式   
   - *forms*     
   &emsp;&emsp;存放forms文件   
   - *common*     
   &emsp;&emsp;存放通用功能，比如日志、json格式化、db等
   - *commands*     
   &emsp;&emsp;自定义flask指令，比如数据库初始化、ipython-shell等   
   - *static*     
   &emsp;&emsp;存放静态资源文件，css/js等
   - *templates*      
   &emsp;&emsp;存放模板文件、Html文件
   - *config*  
   &emsp;&emsp;各环境配置，包括本地、测试、正式环境及各环境通用配置信息
   - *tests*  
   &emsp;&emsp;测试相关文件
   - *requirements*  
   &emsp;&emsp;工程依赖
   - *settings.py*  
   &emsp;&emsp;app配置入口
   - *app_maker.py*  
   &emsp;&emsp;app工厂
   - *app.py*     
   &emsp;&emsp;app入口

## 二. 数据库

&emsp;&emsp;数据库操作方面，没有直接使用`SQLAlchemy`，而是借助针对`Flask`封装了`SQLAlchemy`的`Flask-SQLAlchemy`模块，
使用上更加方便，支持数据库创建、ORM操作等
   
   1. 直接建模，继承flask_sqlalchemy提供的基础模型db.Model
   ```python
    # models.__init__.py
    from flask_sqlalchemy import SQLAlchemy
    from common.utils import import_to_context
    
    # global db
    db = SQLAlchemy()
    
    # 注意这里目的在于导入models目录下所有的python文件中的模型，
    import_to_context('models', locals())
```

   ```python    
    # user.py
    from . import db
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        email = db.Column(db.String(120), unique=True)
    
        def __init__(self, username, email):
            self.username = username
            self.email = email
    
        def __repr__(self):
            return '<User %r>' % self.username
```
   2. 利用sqlacodegen生成已存在数据库表对应的模型
   ```python
    flask-sqlacodegen --flask  --outfile sqlacodegen_tables.py mysql://root:root@localhost:3306/flask
```
   3. 数据库迁移     
   数据库的修改和迁移，我们采用`Flask-Migrate`方案，文档参考：https://flask-migrate.readthedocs.io/en/latest/     
   基本操作如下：      
   ```python
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(128))
    
    # 操作方法   
    pip install Flask-Migrate
    flask db init
    flask db migrate
    flask db upgrade
```

## 三. 自定义指令

&emsp;&emsp;目前已经定义了`3`条自定义指令：
  1. flush drop_tables  
    清空数据库表
  2. flush load_sql
    加载sql文件到db中
  3. flush ipython   
    优先加载ipython作为交互shell，若ipython没有安装则记载默认shell，同时导入db和models
  4. clean   
    清理pyc文件
  5. urls   
    打印路由表
  6. test   
    启动单元测试    

## 四. 配置文件

&emsp;&emsp;目前配置文件入口为工程根目录下的settings.py文件，加载原理为：
从conf.default.py文件中加载通用默认配置，然后根据环境变量`APP_ENV`加载不同环境的自定义配置文件：

```python
本地开发：APP_ENV = develop -> settings_develop.py
测试环境：APP_ENV = test -> settings_test.py
正式环境：APP_ENV = product -> settings_product.py
```
环境配置文件加载后，会覆盖大写同名的默认配置，最终生成完整的配置文件

## 五. app工厂

工厂用于生成实际运行的app，主要组装过程包括：     
```
加载配置-->注册蓝图-->注册扩展-->注册命令-->初始化日志-->初始化db
```

## 六. 工程启动

本地安装依赖后直接启动，生产环境可采用gunicorn或者uwsgi部署
     
```
# 安装依赖，py3环境未验证

pip install -r requirements.txt

# 打开调试模式，代码发生变化时，自动重新加载

export FLASK_APP=app.py
flask run -h 0.0.0.0 -p 5000 --debugger --reload
```
打开本地浏览器，访问：http://127.0.0.1:5000/

## 七. Flask-Admin

提供数据模型的增删改查操作，类似Django-Admin，参考文档：http://flask-admin.readthedocs.io/en/latest/

```python
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView    
    
    # Flask-Admin
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Address, db.session))
    admin.add_view(ModelView(Category, db.session))
    
```

可能会遇到的错误：
> File "c:\python27\lib\site-packages\flask_admin\contrib\sqla\view.py", line 1071, in create_model
model = self.model()
TypeError: __init__() takes exactly 3 arguments (1 given)
 
解决方法：修改model的构造函数，为所有参数提供默认值

```python
    def __init__(self, name):
        self.name = name
```
改为：
```python
    def __init__(self, name=''):
        self.name = name
```


## 八. Flask-Cache

Flask缓存参考链接：https://pythonhosted.org/Flask-Cache/

> Built-in cache types:
null: NullCache (default)
simple: SimpleCache
memcached: MemcachedCache (pylibmc or memcache required)
gaememcached: GAEMemcachedCache
redis: RedisCache (Werkzeug 0.7 required)
filesystem: FileSystemCache
saslmemcached: SASLMemcachedCache (pylibmc required)


```python
cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)

@cache.cached(timeout=50)
def index():
    return render_template('index.html')

@cache.cached(timeout=50, key_prefix='all_comments')
def get_all_comments():
    comments = do_serious_dbio()
    return [x.author for x in comments]

cached_comments = get_all_comments()
```

## 九. 工程依赖

目前工程依赖列表见requirements.txt文件：

```python

# -*- coding: utf-8 -*-


# Flask
Flask==0.12.2
MarkupSafe==1.0
Werkzeug==0.13
Jinja2==2.10
itsdangerous==0.24
click>=5.0

# Database
Flask-SQLAlchemy==2.3.2
psycopg2==2.7.3.2
SQLAlchemy==1.1.15
PyMySQL==0.6.7

# Migrations
Flask-Migrate==2.1.1

# Forms
Flask-WTF==0.14.2
WTForms==2.1

# Deployment
gunicorn>=19.1.1

# Webpack
flask-webpack==0.1.0

# Auth
Flask-Login==0.4.1
Flask-Bcrypt==0.7.1

# Caching
Flask-Caching>=1.0.0

# Debug toolbar
Flask-DebugToolbar==0.10.1

```