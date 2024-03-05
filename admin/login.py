from flask import Blueprint, request, render_template, url_for, session, redirect
from sqlalchemy import select, update
from db.Base import sm
from db.Admin import Admin
from util.util import get_hash256, xss_simple, get_salt, jump

login = Blueprint('login', __name__)


@login.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = xss_simple(request.form['username'])
        password = xss_simple(request.form['password'])
        stmt = select(Admin).where(Admin.username == username)
        result = sm.scalars(stmt).first()
        if not result:
            return jump(session['lang']['username_is_incorrect'], url_for('login.index'))
        if result.failed_count >= 5:
            return jump(session['lang']['too_many_login_fails'], url_for('login.index'))
        token = get_hash256(str(username) + str(password) + str(result.salt))
        if token == result.token:
            salt = get_salt(16)
            token = get_hash256(str(username) + str(password) + str(salt))
            stmt = update(Admin).where(Admin.id == result.id).values(token=token, salt=salt, failed_count=0)
            sm.execute(stmt)
            sm.commit()
            sm.close()
            session['username'] = username
            session['token'] = get_hash256(token)
            session['shell'] = get_hash256(str(session['username']) + get_hash256(session['token']) + salt)
            return redirect(url_for('index'))
        else:
            stmt = update(Admin).where(Admin.id == result.id).values(
                failed_count=result.failed_count + 1
            )
            sm.execute(stmt)
            sm.commit()
            sm.close()
            return jump(session['lang']['password_is_incorrect'], url_for('login.index'))
    return render_template('login/index.html')


@login.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.index'))
