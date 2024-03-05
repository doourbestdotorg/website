import os
import random
import time
import cv2
from flask import render_template, Blueprint, request, url_for, session
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy import select, desc, insert, delete, update
from config.config import config
from db.Base import sm
from db.Say import Say
from util.util import admin_required, date_to_time, xss_simple, jump

say = Blueprint('say', __name__)


@say.route('/')
@admin_required
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    count = sm.query(Say).count()
    stmt = select(Say).where(Say.status >= 0).order_by(desc(Say.id)).offset((page - 1) * per_page).limit(per_page)
    result = sm.scalars(stmt).all()
    sm.close()
    pagination = Pagination(
        page=page,
        total=count,
        per_page=per_page,
        search=search,
        record_name='result'
    )
    return render_template('say/index.html', result=result, pagination=pagination)


@say.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    if request.method == 'POST':
        content = xss_simple(request.form.get('content'))
        img = request.form.getlist('img[]')
        if not img:
            img = []
        img = xss_simple('|'.join(img))
        status = request.form.get('status', 0, int)
        publish_datetime = xss_simple(request.form.get('datetime', ''))
        is_post = request.form.get('is_post', 0, int)
        now = int(time.time())
        if publish_datetime:
            publish_datetime = publish_datetime.replace('T', ' ')
            now = date_to_time(publish_datetime)
        try:
            stmt = insert(Say).values(
                content=content,
                img=img,
                status=status,
                is_post=is_post,
                add_time=now,
                update_time=now
            )
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('say.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('say/add.html')


@say.route('/modify/<int:id>', methods=['GET', 'POST'])
@admin_required
def modify(id):
    stmt = select(Say).where(Say.id == id).where(Say.status >= 0)
    result = sm.scalars(stmt).first()
    result_img = result.img
    if not result_img:
        result_img = []
    else:
        result_img = result_img.split('|')
    if request.method == 'POST':
        content = xss_simple(request.form.get('content'))
        img = request.form.getlist('img[]')
        if not img:
            img = []
        img = xss_simple('|'.join(img))
        status = request.form.get('status', 0, int)
        publish_datetime = xss_simple(request.form.get('datetime', ''))
        is_post = request.form.get('is_post', 0, int)
        now = int(time.time())
        if publish_datetime:
            publish_datetime = publish_datetime.replace('T', ' ')
            now = date_to_time(publish_datetime)
        try:
            stmt = update(Say).where(Say.id == id).where(Say.status >= 0).values(
                content=content,
                img=img,
                status=status,
                is_post=is_post,
                add_time=now
            )
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('say.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template(
        'say/modify.html',
        result=result,
        result_img=result_img
    )


@say.get('/delete/<int:id>')
@admin_required
def deletes(id):
    now = int(time.time())
    try:
        stmt = update(Say).where(Say.status >= 0).where(Say.id == id).values(
            status=-1,
            update_time=now
        )
        sm.execute(stmt)
        sm.commit()
        return jump(session['lang']['success'], url_for('say.index'))
    except Exception as e:
        return str(e)
    finally:
        sm.close()
    # try:
    #     stmt = delete(Say).where(Say.id == id).where(Say.status >= 0)
    #     sm.execute(stmt)
    #     sm.commit()
    #     return jump(session['lang']['success'], url_for('say.index'))
    # except Exception as e:
    #     return str(e)


@say.post('/upload')
@admin_required
def upload():
    upload_dir = config['production'].UPLOAD_DIR
    upload_extension = config['production'].UPLOAD_EXTENSION
    if 'file' not in request.files:
        return {
            'code': -1,
            'message': session['lang']['not_select_file']
        }
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return {
            'code': -2,
            'message': session['lang']['not_select_file']
        }
    if '.' not in file.filename:
        return {
            'code': -3,
            'message': session['lang']['not_select_file']
        }
    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext in upload_extension:
        filename_base = str(time.strftime('%Y%m%d%H%M%S')) + str(random.randint(1000, 9999))
        filename = filename_base + '.' + ext
        filename_thumbnail = filename_base + '_thumbnail.' + ext
        current_dir = os.path.join(upload_dir, 'say')
        if not os.path.exists(current_dir) or not os.path.isdir(current_dir):
            os.makedirs(current_dir)
        absolute_filename = os.path.join(current_dir, filename)
        absolute_filename_thumbnail = os.path.join(current_dir, filename_thumbnail)
        relative_filename_thumbnail = absolute_filename_thumbnail.replace(os.getcwd(), '')
        file.save(absolute_filename)
        compress_image(absolute_filename, absolute_filename_thumbnail)
        return {
            'code': 0,
            'message': relative_filename_thumbnail.replace('\\', '/')
        }
    else:
        return {
            'code': -3,
            'message': session['lang']['illegal_files']
        }


def compress_image(file, file1):
    im = cv2.imread(file)
    img_height, img_width = im.shape[:2]
    thumbnail_width = config['production'].SAY_THUMBNAIL_WIDTH
    thumbnail_height = config['production'].SAY_THUMBNAIL_HEIGHT
    thumbnail_ratio = config['production'].SAY_THUMBNAIL_RATIO
    if img_width <= thumbnail_width and img_height <= thumbnail_height:
        cv2.imwrite(file1, im)
    else:
        # coordinate
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        if (img_width * thumbnail_ratio) > img_height:
            width = int(img_height / thumbnail_ratio)  # valid width
            x1 = int((img_width - width) / 2)
            x2 = x1 + width
            y1 = 0
            y2 = img_height
        else:
            x1 = 0
            x2 = img_width
            height = int(img_width * thumbnail_ratio)  # valid height
            y1 = int((img_height - height) / 2)
            y2 = y1 + height
        print(x1, x2, y1, y2)
        im1 = im[y1:y2, x1:x2]
        resized_image = cv2.resize(im1, (thumbnail_width, thumbnail_height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(file1, resized_image)
