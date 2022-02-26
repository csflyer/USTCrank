## 1. USTCrank
基于 `python3` + `Flask` + `BeautifulSoup`, 用于统计 USTC 考研初试的成绩排名, 其他学校如有需要也可以在本系统上修改实现需求。
1. 报考 USTC 的所有同学均可登录查分，不只限于CS相关专业，可查看本专业排名，人数越多，数据越准确

2. 网站仅保存分数相关信息，无需担心泄露隐私

3. 用户凭账户密码登录后方可查看排名, 防止只围观不录分

4. 历史数据在scores文件夹下, 提供sqlite3数据库文件与html table文件

5. **master分支支持各种关系性数据库，使用 `flask_sqlalchemy` 作为orm (master分支的配置与部署请查看master分支的 `README.md` 文件);
    出于性能考虑,新增加的mongo分支使用 `Mongodb` 作为数据库，orm为 `mongoengine`，推荐使用此分支;**

## 2. 历史更新记录
1. 2020-03-07 增加登录机制，只有查分后才能查看排名

2. 2020-04-11 网站下线,总录分849条

3. 2021-02-26 新增加mongo分支可使用 `Mongodb` 作为数据库

4. 2021-02-27 mongo分支支持创建围观账户(可登陆查看排名，但无法修改密码), 其他功能请查看 `manage.py`

* 操作：进入源码目录和虚拟环境，运行 `python manage.py shell`, 调用`create_super_user(kaohao, password)` 函数即可

* 注意: kaohao为准考证号，必须为15位长度；password 为密码，必须为6位; 建议kaohao使用为0或接近0的字符串

* 实例: `create_super_user("000000000000000", "123456")`

5. 2021-03-28 网站下线,总录分3049条

6. 2022-02-26 按照学院专业和考试各科目名称进行排名，而不再是只根据学院专业排名

## 3. 本地运行
1. 安装 `mongodb` (版本>=3.4.6), 并修改 `app/__init__.py` 中的数据库路径 即 `app.config['MONGODB_SETTINGS']` 中的内容',如使用其他数据库请搜索修改

2. 运行 `pip install -r requirements/pip.txt` 安装所有依赖库, 并设置好环境变量 `SECRET_KEY` 为一个私密的字符串

3. 最后运行 `python manage.py run` 即可

## 4. 服务器部署
1. 使用 `pip3 install virtualenv` 安装 `virtualenv` , 如失败则运行 `python -m pip install --upgrade pip` 将 `pip` 升级到最新版本再尝试

2. 进入项目文件夹, 运行 `virtualenv venv` 创建虚拟环境

3. 安装依赖包 运行 `source venv/bin/activate` 激活虚拟环境(后续操作均在虚拟环境下进行)， 再运行 `pip install -r requirements/pip.txt` 安装所有依赖

4. 安装mongodb(版本>=3.4.6), 并修改 `app/__init__.py` 中的数据库路径 即 `app.config['MONGODB_SETTINGS']` 中的内容; 设置好环境变量 `SECRET_KEY` 为一个私密的字符串，且以后不能改动。

5. 使用 `gunicorn` 作为 web服务器， 使用 `pip install gunicorn` 安装 `gunicorn`

6. 运行 `gunicorn --workers=5 -b 0.0.0.0:80 manage:app` 即可启动站点, 具体参数请百度

## 5. 声明
    本代码仅供学习交流，用户使用所造成的不良后果与作者无关