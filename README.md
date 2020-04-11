## 1. USTCrank
    基于python3 + Flask + BeautifulSoup, 用于统计 USTC 考研初试的成绩排名
    1.1 报考 USTC 的所有同学均可登录查分，不只限于CS相关专业，可查看本专业排名，人数越多，数据越准确
    1.2 网站仅保存分数相关信息，无需担心泄露隐私
    1.3 用户凭账户密码登录后方可查看排名, 防止只围观不录分
    1.4 历史数据在scores文件夹下, 提供sqlite3数据库文件与html table文件
    update:
        2020-03-07 增加登录机制，只有查分后才能查看排名
        2020-04-11 网站下线,总录分849条

## 2. 本地运行准备
    1. 修改 app/__init__.py 中的数据库路径 即 app.config['SQLALCHEMY_DATABASE_URI']后面的值，应为'sqlite:///路径'.
    2. 运行 pip install -r requirements/pip.txt 安装所有依赖库
    3. 如第一次运行或未创建数据库，则运行 python manage.py shell 然后输入 db.create_all() 创建数据库
    4. 最后运行 python manage.py run 即可


## 3. 服务器部署
    1. 使用 pip3 install virtualenv 安装virtualenv, 如失败则运行 python -m pip install --upgrade pip 将 pip 升级到最新版本再尝试
    2. 进入项目文件夹, 运行 virtualenv venv 创建虚拟环境
    3. 安装依赖包 运行 source venv/bin/activate 激活虚拟环境(后续操作均在虚拟环境下进行)， 再运行 pip install -r requirements/pip.txt 安装所有依赖
    4. 如第一次运行或未创建数据库，修改 app/__init__.py 中的数据库路径，再运行 python manage.py shell 然后输入 db.create_all() 创建数据库
    5. 使用 gunicorn 作为 web服务器， 使用 pip install gunicorn 安装 gunicorn
    6. 运行 gunicorn --workers=5 -b 0.0.0.0:80 manage:app 即可启动站点, 具体参数请百度

## 3. 声明
    本代码仅供学习交流，用户使用所造成的不良后果与作者无关
