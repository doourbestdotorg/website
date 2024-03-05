from flask import render_template, Blueprint, request, session, abort
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy import select, desc
from db.Category import Category
from db.Article import Article
from db.Base import sm

article = Blueprint('article', __name__)


# list page
# id:category_id
@article.get('/<int:id>')
def index(id):
    stmt_category = select(Category).where(Category.id == id).where(Category.status == 1)
    result_category = sm.scalars(stmt_category).first()
    if not result_category:
        return abort(404)
    list_style=result_category.list_style
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = int(session['setting']['each_page_number'])
    count = sm.query(Article).where(Article.status==1).count()
    stmt = select(Article).where(Article.status==1).where(Article.category_id == id).order_by(desc(Article.id)).offset(
        (page - 1) * per_page).limit(per_page)
    result = sm.scalars(stmt).all()
    result_recommend=None
    if list_style=='row':
        limit_number=int(session['setting']['each_page_recommend_number'])
        stmt_recommend = select(Article).where(Article.status==1).where(Article.id != id).order_by(desc(Article.sort)).limit(limit_number)
        result_recommend = sm.scalars(stmt_recommend).all()
    sm.close()
    pagination = Pagination(
        page=page,
        total=count,
        per_page=per_page,
        search=search,
        record_name='result'
    )
    return render_template(
        'article/index_'+list_style+'.html',
        result=result,
        pagination=pagination,
        list_style=list_style,
        result_recommend=result_recommend
    )


@article.get('/content/<int:id>')
def content(id):
    stmt = select(Article).where(Article.status==1).where(Article.id == id).where(Article.status == 1)
    result = sm.scalars(stmt).first()
    limit_number = int(session['setting']['each_page_recommend_number'])
    stmt_recommend = select(Article).where(Article.id != id).order_by(desc(Article.sort)).limit(limit_number)
    result_recommend = sm.scalars(stmt_recommend).all()
    return render_template('article/content.html', result=result, result_recommend=result_recommend)
