import json
import time
from flask import Flask, render_template, redirect, abort, session
from sqlalchemy import select, asc
from config.config import config
from db.Base import sm
from db.Navigation import Navigation
from db.Setting import Setting
from home.about import about
from home.article import article
from home.say import say
from lang.lang import *

app = Flask(__name__, template_folder='templates/home')


@app.get('/')
def index():
    stmt = select(Navigation).where(Navigation.status == 1).order_by(asc(Navigation.sort))
    result = sm.scalars(stmt).first()
    sm.close()
    if result:
        return redirect(result.url)
    return render_template('index/index.html')


@app.template_filter('time_to_datetime')
def time_to_datetime(time_number):
    time_number = int(time_number)
    x = time.localtime(time_number)
    return time.strftime('%Y-%m-%d %H:%M:%S', x)


@app.template_filter('str_to_dict')
def str_to_dict(s):
    return json.loads(s)


app.config.from_object(config['production'])
app.jinja_env.filters['time_to_datetime'] = time_to_datetime
app.jinja_env.filters['str_to_dict'] = str_to_dict
app.register_blueprint(article, url_prefix='/article')
app.register_blueprint(about, url_prefix='/about')
app.register_blueprint(say, url_prefix='/say')


@app.before_request
def before_request():
    if 'navigation' not in session:
        stmt = select(Navigation).where(Navigation.status == 1).order_by(asc(Navigation.sort))
        result = sm.scalars(stmt).all()
        lists = []
        for r in result:
            lists.append(r.to_dict())
        session['navigation'] = json.dumps(lists)
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


# error page 404
@app.errorhandler(404)
def error_404(error):
    return render_template('base/404.html'), 404


# error page 500
@app.errorhandler(500)
def error_500(error):
    return render_template('base/500.html'), 500


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=7001,
        debug=False
    )
