import time
from flask import render_template, Blueprint, request, url_for, session
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy import select, desc, insert, update, asc
from db.Article import Article
from db.Base import sm
from db.Category import Category
from util.util import admin_required, xss_simple, xss_rich, jump

article = Blueprint('article', __name__)


@article.route('/')
@admin_required
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    count = sm.query(Article).count()
    stmt = select(Article).where(Article.status >= 0).order_by(desc(Article.id)).offset((page - 1) * per_page).limit(
        per_page)
    result = sm.scalars(stmt).all()
    sm.close()
    pagination = Pagination(
        page=page,
        total=count,
        per_page=per_page,
        search=search,
        record_name='result'
    )
    return render_template('article/index.html', result=result, pagination=pagination)


@article.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    stmt_category = select(Category).where(Category.status == 1).order_by(asc(Category.sort))
    result_category = sm.scalars(stmt_category).all()
    if request.method == 'POST':
        category_id = request.form.get('category', 0, int)
        title = xss_simple(request.form.get('title'))
        keyword = xss_simple(request.form.get('keyword'))
        description = xss_simple(request.form.get('description'))
        video = xss_simple(request.form.get('video'))
        sort = request.form.get('sort', 0, int)
        thumbnail = xss_simple(request.form.get('thumbnail'))
        content = xss_rich(request.form.get('content'))
        status = request.form.get('status', 0, int)
        from_title = xss_simple(request.form.get('from_title'))
        from_url = xss_simple(request.form.get('from_url'))
        now = int(time.time())
        try:
            stmt = insert(Article).values(
                category_id=category_id,
                title=title,
                keyword=keyword,
                description=description,
                video=video,
                sort=sort,
                thumbnail=thumbnail,
                content=content,
                status=status,
                from_title=from_title,
                from_url=from_url,
                add_time=now,
                update_time=now
            )
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('article.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('article/add.html', result_category=result_category)


@article.route('/modify/<int:id>', methods=['GET', 'POST'])
@admin_required
def modify(id):
    stmt_category = select(Category).where(Category.status == 1).order_by(asc(Category.sort))
    result_category = sm.scalars(stmt_category).all()
    stmt = select(Article).where(Article.id == id).where(Article.status >= 0)
    result = sm.scalars(stmt).first()
    if request.method == 'POST':
        category_id = request.form.get('category', 0, int)
        title = xss_simple(request.form.get('title'))
        keyword = xss_simple(request.form.get('keyword'))
        description = xss_simple(request.form.get('description'))
        video = xss_simple(request.form.get('video'))
        sort = request.form.get('sort', 0, int)
        thumbnail = xss_simple(request.form.get('thumbnail'))
        content = xss_rich(request.form.get('content'))
        # content = request.form.get('content')
        status = request.form.get('status', 0, int)
        from_title = xss_simple(request.form.get('from_title'))
        from_url = xss_simple(request.form.get('from_url'))
        now = int(time.time())
        try:
            stmt = update(Article).values(
                category_id=category_id,
                title=title,
                keyword=keyword,
                description=description,
                video=video,
                sort=sort,
                thumbnail=thumbnail,
                content=content,
                status=status,
                from_title=from_title,
                from_url=from_url,
                update_time=now
            ).where(Article.id == id)
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('article.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('article/modify.html', result=result, result_category=result_category)


@article.get('/delete/<int:id>')
@admin_required
def deletes(id):
    now = int(time.time())
    try:
        stmt = update(Article).where(Article.status >= 0).where(Article.id == id).values(
            status=-1,
            update_time=now
        )
        sm.execute(stmt)
        sm.commit()
        return jump(session['lang']['success'], url_for('article.index'))
    except Exception as e:
        return str(e)
    finally:
        sm.close()
