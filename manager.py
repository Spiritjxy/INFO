from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from info import create_app, db

app = create_app('develop')
# 创建manager，关联app
manager = Manager(app)
# 关联app，db
Migrate(app, db)
# 添加操作命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
