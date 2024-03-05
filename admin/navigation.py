from flask import render_template, Blueprint, request, url_for, session
from sqlalchemy import insert, select, update, asc
from db.Base import sm
from db.Navigation import Navigation
from util.util import admin_required, xss_simple, jump

navigation = Blueprint('navigation', __name__)


@navigation.route('/')
@admin_required
def index():
    stmt = select(Navigation).where(Navigation.status >= 0).order_by(asc(Navigation.sort))
    result = sm.scalars(stmt).all()
    return render_template('navigation/index.html', result=result)


@navigation.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    if request.method == 'POST':
        title = xss_simple(request.form.get('title'))
        url = xss_simple(request.form.get('url'))
        sort = request.form.get('sort', 0, int)
        status = request.form.get('status', 0, int)
        try:
            stmt = insert(Navigation).values(
                title=title,
                url=url,
                sort=sort,
                status=status
            )
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('navigation.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('navigation/add.html')


@navigation.route('/modify/<int:id>', methods=['GET', 'POST'])
@admin_required
def modify(id):
    stmt = select(Navigation).where(Navigation.status >= 0).where(Navigation.id == id)
    result = sm.scalars(stmt).first()
    if request.method == 'POST':
        title = xss_simple(request.form.get('title'))
        url = xss_simple(request.form.get('url'))
        sort = request.form.get('sort', 0, int)
        status = request.form.get('status', 0, int)
        try:
            stmt = update(Navigation).values(
                title=title,
                url=url,
                sort=sort,
                status=status
            ).where(Navigation.status >= 0).where(Navigation.id == id)
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('navigation.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('navigation/modify.html', result=result)


@navigation.get('/delete/<int:id>')
@admin_required
def delete(id):
    pass
