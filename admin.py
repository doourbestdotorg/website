import time
from flask import Flask, render_template, request, session
from sqlalchemy import select
from admin.about import about
from admin.admin import admin
from admin.article import article
from admin.category import category
from admin.login import login
from admin.navigation import navigation
from admin.tinymce import tinymce
from admin.say import say
from admin.setting import setting
from admin.upload import upload
from db.Base import sm
from db.Setting import Setting
from util.util import admin_required, xss_simple
from config.config import config
from lang.lang import *

app = Flask(__name__, template_folder='templates/admin')


@app.template_filter('cut_str')
def cur_str(s):
    if len(s) > config['production'].ADMIN_CUT_STRING_LENGTH:
        s = s[:config['production'].ADMIN_CUT_STRING_LENGTH] + '...'
    return s


@app.template_filter('time_to_datetime')
def time_to_datetime(time_number):
    time_number = int(time_number)
    x = time.localtime(time_number)
    return time.strftime('%Y-%m-%d %H:%M:%S', x)


app.config.from_object(config['production'])
app.jinja_env.filters['cur_str'] = cur_str
app.jinja_env.filters['time_to_datetime'] = time_to_datetime
app.register_blueprint(about, url_prefix='/about')
app.register_blueprint(article, url_prefix='/article')
app.register_blueprint(tinymce, url_prefix='/tinymce')
app.register_blueprint(say, url_prefix='/say')
app.register_blueprint(category, url_prefix='/category')
app.register_blueprint(navigation, url_prefix='/navigation')
app.register_blueprint(setting, url_prefix='/setting')
app.register_blueprint(upload, url_prefix='/upload')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(admin, url_prefix='/admin')


@app.before_request
def before_request():
    if 'setting' not in session:
        stmt = select(Setting)
        result = sm.scalars(stmt).all()
        dicts = {}
        for r in result:
            dicts.update({r.key: r.value})
        session['setting'] = dicts
    if 'lang' not in session:
        language = session['setting']['language']
        session['lang'] = eval(language)


@app.after_request
def disable_caching(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Expires'] = '-1'
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/')
@admin_required
def index():
    return render_template('index/index.html')


# error page 404
@app.errorhandler(404)
def error_404(error):
    return render_template('base/404.html'), 404


# error page 500
@app.errorhandler(500)
def error_500(error):
    return render_template('base/500.html'), 500


@app.route('/jump')
def jump():
    message = xss_simple(request.args.get('message'))
    jump_url = xss_simple(request.args.get('jump_url'))
    last_time = request.args.get('last_time', 3, int)
    return render_template('base/jump.html', message=message, jump_url=jump_url, last_time=last_time)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=7002,
        debug=False
    )
