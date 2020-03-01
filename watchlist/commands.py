import click
from watchlist import app, db
from watchlist.models import User, Articles


@app.cli.command()
@click.option('--drop', is_flag=True, help='删除之后再创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库')


@app.cli.command()
def forge():
    db.create_all()
    movies = ['苏亮', '2020.3.1', 1]
    for m in range(10):
        movie = Articles(title=movies[0], content=str(m)*10, pubdate=movies[1], author_id=movies[2])
        db.session.add(movie)
    click.echo('数据导入完成')


@app.cli.command()
@click.option('--username', prompt=True, help="用来登录的用户名")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="用来登录的密码")
def admin(username, password):
    db.create_all()
    if all([username, password]) and not User.query.filter_by(username=username).first():
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
    else:
        click.echo('未成功创建,原因可能是重复或者信息填写错误')
        exit()

    click.echo('创建管理员账号完成')
