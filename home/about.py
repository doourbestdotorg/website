from flask import render_template, Blueprint, session
from sqlalchemy import select, desc
from db.About import About
from db.Article import Article
from db.Base import sm

about = Blueprint('about', __name__)


@about.get('/content/<int:id>')
def content(id):
    stmt = select(About).where(About.id == id).where(About.status == 1)
    result = sm.scalars(stmt).first()
    limit_number = int(session['setting']['each_page_recommend_number'])
    stmt_recommend = select(Article).where(Article.id != id).order_by(desc(Article.sort)).limit(limit_number)
    result_recommend = sm.scalars(stmt_recommend).all()
    return render_template('about/content.html', result=result, result_recommend=result_recommend)
