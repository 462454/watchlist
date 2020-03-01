from watchlist import app, db
from flask import jsonify, request, render_template, make_response, redirect, url_for
from flask_login import login_required, current_user, logout_user, login_user
from watchlist.models import Articles, User
from .sqltodict import queryToDict
from datetime import datetime
from re import sub


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if not current_user.is_authenticated:
#             return redirect(url_for('index'))
#         title = request.form.get('title')
#         year = request.form.get('year')
#
#         if not title or not year or len(year) > 4 or len(title) > 60:
#             flash('输入错误')
#             return redirect(url_for('index'))
#
#         movie = Articles(title=title, year=year)
#         db.session.add(movie)
#         flash('数据创建成功')
#         return redirect(url_for('index'))
#
#     movies = Articles.query.all()
#     return render_template('index.html', movies=movies)
#
#
# @app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
# @login_required
# def edit(movie_id):
#     movie = Articles.query.get_or_404(movie_id)
#
#     if request.method == 'POST':
#         title = request.form['title']
#         year = request.form['year']
#
#         if not title or not year or len(year) > 4 or len(title) > 60:
#             flash('输入错误')
#             return redirect(url_for('edit'), movie_id=movie_id)
#
#         movie.title = title
#         movie.year = year
#
#         flash('电影信息已经更新')
#         return redirect(url_for('index'))
#     return render_template('edit.html', movie=movie)
#
#
# @app.route('/settings', methods=['GET', 'POST'])
# @login_required
# def settings():
#     if request.method == 'POST':
#         name = request.form['name']
#
#         if not name or len(name) > 20:
#             flash('输入错误')
#             return redirect(url_for('settings'))
#
#         current_user.name = name
#
#         flash('设置name成功')
#         return redirect(url_for('index'))
#
#     return render_template('settings.html')
#
#
# @app.route('/movie/delete/<int:movie_id>', methods=['POST'])
# @login_required
# def delete(movie_id):
#     movie = Articles.query.get_or_404(movie_id)
#     db.session.delete(movie)
#
#     flash('删除数据成功')
#     return redirect(url_for('index'))
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         if not username or not password:
#             flash('输入错误')
#             return redirect(url_for('login'))
#         user = User.query.first()
#         if username == user.username and user.validate_password(password):
#             login_user(user)
#             flash('登录成功')
#             return redirect(url_for('index'))
#         flash('用户名或密码输入错误')
#         return redirect(url_for('login'))
#     return render_template('login.html')
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('退出登录')
#     return redirect(url_for('index'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/article/<int:id_>', methods=['GET'])
def detail(id_):
    article = Articles.query.filter_by(id=id_)[0]
    return render_template('detail.html', info=article)


@app.route('/new_articles/<int:number>', methods=['GET'])
def new_articles(number):
    articles = Articles.query.all()[-1:-number - 1:-1]
    return jsonify(queryToDict(articles))


@app.route('/user_articles', methods=['GET'])
@login_required
def user_articles():
    articles = Articles.query.filter_by(author_id=1)[::-1][:3]
    return jsonify(queryToDict(articles))


@app.route('/page/<int:num>', methods=['GET'])
def page(num):
    articles = Articles.query.all()[-1::-1][(num - 1) * 5:num * 5]
    flag = False
    if len(Articles.query.all()[num * 5:]) > 0:
        flag = True
    return jsonify(queryToDict(articles) + [flag])


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.values['username']
        password = request.values['password']
        if not username or not password:
            return jsonify(False)
        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            login_user(user)
            return jsonify(True)
        return jsonify(False)


@app.route('/logout', methods=['OPTIONS'])
@login_required
def logout():
    logout_user()
    return jsonify(True)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.values['title']
        content = sub(r'\s', '', request.values['content'])
        article = Articles(title=title, content=content, pubdate=datetime.now().date(), author_id=current_user.id)
        db.session.add(article)
        return jsonify(True)
    return render_template('create.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    return
