from watchlist import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', information='很抱歉，你找的页面不存在'), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html', information='请求错误'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', information='服务器内部错误'), 500
