# 1. USTCrank
    基于python3, Flask, BeautifulSoup， 作者QQ：924105150

# 2. 本地运行准备
    1. 修改 app/__init__.py 中的数据库路径 即 app.config['SQLALCHEMY_DATABASE_URI']后面的值，应为'sqlite:///路径'.
    2. 运行 pip install -r requirements/pip.txt 安装所有依赖库
    3. 如第一次运行或未创建数据库，则运行 python manage.py shell 然后输入 db.create_all() 创建数据库
    4. 最后运行 python manage.py run 即可

# 3. 声明
    本代码仅供学习交流，用户使用所造成的不良后果与作者无关
