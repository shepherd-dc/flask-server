'''
数据库迁移表时报错：alembic.util.exc.CommandError: Target database is not up to date.
解决方法：
1. 先到项目目录下的migrations/version下，找到最新的migrate版本号。
2. 然后更新数据库中的alembic_version表的version_num字段的值为最新migrate版本号。
update alembic_version set version_num = '版本号';
3. 之后就可以正常的migrate和upgrade了。
'''

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.models.base import db

app = create_app()
manager = Manager(app)

# 1. 要使用flask_migrate,必须绑定app和db
migrate = Migrate(app, db)
# 2. 把MigrateCommand命令添加到manager中
manager.add_command('db', MigrateCommand)
# 3. 命令行命令: 模型 -> 迁移文件 -> 表
## 1）python manage.py db init 初始化迁移环境，只需执行一次
## 2) python manage.py db migrate 将模型生成迁移文件，只要模型更改就需执行
## 3) python manage.py db upgrade 将迁移文件真正映射到数据表中，每次生成完迁移文件就需执行


@manager.command
def runserver():
    print('Server is running...')


if __name__ == '__main__':
    manager.run()