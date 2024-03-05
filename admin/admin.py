from flask import Blueprint, request, render_template, url_for, session
from sqlalchemy import select, update

from db.Base import sm
from db.Admin import Admin
from util.util import get_hash256, xss_simple, get_salt, jump, admin_required

admin = Blueprint('admin', __name__)


@admin.route('/', methods=['GET', 'POST'])
@admin_required
def index():
    if request.method == 'POST':
        username = xss_simple(request.form['username'])
        password = xss_simple(request.form['password'])
        stmt = select(Admin).where(Admin.username == session['username'])
        result = sm.scalars(stmt).first()
        salt = get_salt(16)
        token = get_hash256(str(username) + str(password) + str(salt))
        stmt = update(Admin).where(Admin.id == result.id).values(
            username=username,
            token=token,
            salt=salt,
            failed_count=0
        )
        sm.execute(stmt)
        sm.commit()
        sm.close()
        session['username'] = username
        session['token'] = get_hash256(token)
        session['shell'] = get_hash256(str(session['username']) + get_hash256(session['token']))
        return jump(session['lang']['success'], url_for('index'))
    return render_template('admin/index.html')