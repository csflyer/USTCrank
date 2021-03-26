## 1. USTCrank
基于 `python3` + `Flask` + `BeautifulSoup`, 用于统计 USTC 考研初试的成绩排名
1. 报考 USTC 的所有同学均可登录查分，不只限于CS相关专业，可查看本专业排名，人数越多，数据越准确**

2. 网站仅保存分数相关信息，无需担心泄露隐私

3. 用户凭账户密码登录后方可查看排名, 防止只围观不录分

4. 历史数据在scores文件夹下, 提供sqlite3数据库文件与html table文件

5. ** `master`分支支持各种关系性数据库，使用 `flask_sqlalchemy` 作为orm;
    出于性能考虑,新增加的mongo分支使用 `Mongodb` 作为数据库，orm为 `mongoengine`，推荐使用mongo分支(mongo分支的配置部署请查看mongo分支的 `README.md`文件) **

## 2. 历史更新记录
1. 2020-03-07 增加登录机制，只有查分后才能查看排名

2. 2020-04-11 网站下线,总录分849条

3. 2021-02-26 新增加mongo分支可使用 `Mongodb` 作为数据库

## 3. 本地运行
1. 修改 `app/__init__.py` 中的数据库路径 即 `app.config['SQLALCHEMY_DATABASE_URI']` 后面的值，如使用sqlite则应为`'sqlite:///路径'` ,如使用其他数据库请搜索修改

2. 运行 `pip install -r requirements/pip.txt` 安装所有依赖库，并设置好环境变量 `SECRET_KEY` 为一个私密的字符串

3. 如第一次运行或未创建数据库，则运行 `python manage.py shell`, 然后输入 `db.create_all()` 创建数据库

4. 最后运行 `python manage.py run` 即可

## 4. 服务器部署
1. 使用 `pip3 install virtualenv` 安装 `virtualenv`, 如失败则运行 `python -m pip install --upgrade pip` 将 `pip` 升级到最新版本再尝试

2. 进入项目文件夹, 运行 `virtualenv venv` 创建虚拟环境

3. 安装依赖包 运行 `source venv/bin/activate` 激活虚拟环境(后续操作均在虚拟环境下进行)， 再运行 `pip install -r requirements/pip.txt` 安装所有依赖。设置好环境变量 `SECRET_KEY` 为一个私密的字符串，且以后不能改动。

4. 如第一次运行或未创建数据库，修改 `app/__init__.py` 中的数据库路径(极度不推荐正式环境使用sqlite)，再运行 `python manage.py shell` 然后输入 `db.create_all()` 创建数据库

5. 使用 `gunicorn` 作为 web服务器， 使用 `pip install gunicorn` 安装 `gunicorn`

6. 运行 `gunicorn --workers=5 -b 0.0.0.0:80 manage:app` 即可启动站点, 具体参数请百度

## 5. 声明
    本代码仅供学习交流，用户使用所造成的不良后果与作者无关

 最后说一下整个项目，即使数据库换成 `mongodb`，项目实际并发能力也非常有限，主要是因为同步地去执行查询成绩，获取验证码等高耗时操作，后续优化方向:
 1. 改成前后端分离
 2. 后端加入任务队列, 前端提交任务，后端插入任务队列，前端周期性去查询任务状态，可参考[Python Web：Flask异步执行任务](https://juejin.cn/post/6844903944762687502)

 这个项目后续大概率不会有大更新了, 以上意见仅供参考。欢迎各位有能力的大佬能写出性能更好的项目，USTC能提供排名那就更好了。