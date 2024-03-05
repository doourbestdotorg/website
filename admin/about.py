from flask import render_template, Blueprint, request, url_for, session
from sqlalchemy import insert, select, update, desc
from util.util import admin_required, xss_simple, xss_rich, jump
from db.About import About
from db.Base import sm
from flask_paginate import Pagination, get_page_parameter

about = Blueprint('about', __name__)


@about.route('/')
@admin_required
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    count = sm.query(About).count()
    stmt = select(About).where(About.status >= 0).order_by(desc(About.id)).offset((page - 1) * per_page).limit(per_page)
    result = sm.scalars(stmt).all()
    sm.close()
    pagination = Pagination(
        page=page,
        total=count,
        per_page=per_page,
        search=search,
        record_name='result'
    )
    return render_template('about/index.html', result=result, pagination=pagination)


@about.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    if request.method == 'POST':
        title = xss_simple(request.form.get('title'))
        keyword = xss_simple(request.form.get('keyword'))
        description = xss_simple(request.form.get('description'))
        video = xss_simple(request.form.get('video'))
        sort = request.form.get('sort', 0, int)
        content = xss_rich(request.form.get('content'))
        status = request.form.get('status', 0, int)
        try:
            stmt = insert(About).values(
                title=title,
                keyword=keyword,
                description=description,
                video=video,
                sort=sort,
                content=content,
                status=status
            )
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('about.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('about/add.html')


@about.route('/modify/<int:id>', methods=['GET', 'POST'])
@admin_required
def modify(id):
    stmt = select(About).where(About.id == id).where(About.status >= 0)
    result = sm.scalars(stmt).first()
    if request.method == 'POST':
        title = xss_simple(request.form.get('title'))
        keyword = xss_simple(request.form.get('keyword'))
        description = xss_simple(request.form.get('description'))
        video = xss_simple(request.form.get('video'))
        sort = request.form.get('sort', 0, int)
        content = xss_rich(request.form.get('content'))
        status = request.form.get('status', 0, int)
        try:
            stmt = update(About).values(
                title=title,
                keyword=keyword,
                description=description,
                video=video,
                sort=sort,
                content=content,
                status=status
            ).where(About.id == id)
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('about.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('about/modify.html', result=result)


@about.get('/delete/<int:id>')
@admin_required
def deletes(id):
    try:
        stmt = update(About).where(About.status >= 0).where(About.id == id).values(
            status=-1
        )
        sm.execute(stmt)
        sm.commit()
        return jump(session['lang']['success'], url_for('about.index'))
    except Exception as e:
        return str(e)
    finally:
        sm.close()
