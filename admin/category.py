from flask import render_template, Blueprint, request, url_for, abort, session
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy import insert, select, update, desc
from config.config import config
from db.Base import sm
from db.Category import Category
from util.util import admin_required, xss_simple, jump

category = Blueprint('category', __name__)


@category.route('/')
@admin_required
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    count = sm.query(Category).count()
    stmt = select(Category).order_by(desc(Category.id)).offset((page - 1) * per_page).limit(per_page)
    result = sm.scalars(stmt).all()
    sm.close()
    pagination = Pagination(
        page=page,
        total=count,
        per_page=per_page,
        search=search,
        record_name='result'
    )
    return render_template('category/index.html', result=result, pagination=pagination)


@category.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    if request.method == 'POST':
        title = xss_simple(request.form.get('title'))
        list_style = xss_simple(request.form.get('list_style'))
        if list_style not in config['production'].LIST_STYLE:
            return abort(404)
        sort = request.form.get('sort', 0, int)
        status = request.form.get('status', 0, int)
        try:
            stmt = insert(Category).values(
                title=title,
                list_style=list_style,
                sort=sort,
                status=status
            )
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('category.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('category/add.html')


@category.route('/modify/<int:id>', methods=['GET', 'POST'])
@admin_required
def modify(id):
    stmt = select(Category).where(Category.id == id).where(Category.status >= 0)
    result = sm.scalars(stmt).first()
    if request.method == 'POST':
        title = xss_simple(request.form.get('title'))
        list_style = xss_simple(request.form.get('list_style'))
        if list_style not in config['production'].LIST_STYLE:
            return abort(404)
        sort = request.form.get('sort', 0, int)
        status = request.form.get('status', 0, int)
        try:
            stmt = update(Category).values(
                title=title,
                list_style=list_style,
                sort=sort,
                status=status
            ).where(Category.id == id)
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('category.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('category/modify.html', result=result)
