from flask import render_template, Blueprint, request, session
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy import select, desc
from db.Article import Article
from db.Base import sm
from db.Say import Say

say = Blueprint('say', __name__)


# list page
# id:category_id
@say.get('/')
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # per_page = int(session['setting']['each_page_number'])
    per_page = 20
    count = sm.query(Say).where(Say.status == 1).count()
    stmt = select(Say).where(Say.status == 1).order_by(desc(Say.id)).offset((page - 1) * per_page).limit(per_page)
    result = sm.scalars(stmt).all()
    lists = []
    for r in result:
        lists.append(r.to_dict())
    limit_number = int(session['setting']['each_page_recommend_number'])
    stmt_recommend = select(Article).where(Article.id != id).order_by(desc(Article.sort)).limit(limit_number)
    result_recommend = sm.scalars(stmt_recommend).all()
    sm.close()
    pagination = Pagination(
        page=page,
        total=count,
        per_page=per_page,
        search=search,
        record_name='result'
    )
    return render_template('say/index.html', result=lists, pagination=pagination, result_recommend=result_recommend)


@say.get('/content/<int:id>')
def content(id):
    pass
    stmt = select(Say).where(Say.id == id).where(Say.status == 1)
    result = sm.scalars(stmt).first()
    img_arr = []
    if result:
        img = result.img
        img_arr = img.split('|')
    img_arr_len = len(img_arr)
    limit_number = int(session['setting']['each_page_recommend_number'])
    stmt_recommend = select(Article).where(Article.id != id).order_by(desc(Article.sort)).limit(limit_number)
    result_recommend = sm.scalars(stmt_recommend).all()
    return render_template('say/content.html', result=result, result_recommend=result_recommend, img_arr=img_arr,
                           img_arr_len=img_arr_len)
