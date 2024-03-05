import os
import random
import time
import cv2
from flask import render_template, Blueprint, request, url_for, session
from sqlalchemy import select, asc, update
from config.config import config
from db.Base import sm
from db.Setting import Setting
from util.util import admin_required, xss_simple, jump
from lang.lang import *

setting = Blueprint('setting', __name__)


@setting.route('/')
@admin_required
def index():
    stmt = select(Setting).order_by(asc(Setting.id))
    result = sm.scalars(stmt).all()
    return render_template('setting/index.html', result=result)


@setting.route('/modify/<int:id>', methods=['GET', 'POST'])
@admin_required
def modify(id):
    stmt = select(Setting).where(Setting.id == id)
    result = sm.scalars(stmt).first()
    if request.method == 'POST':
        value = xss_simple(request.form.get('value', ''))
        try:
            stmt = update(Setting).values(
                value=value
            ).where(Setting.id == id)
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('setting.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('setting/modify.html', result=result)


@setting.route('/modify_language', methods=['GET', 'POST'])
@admin_required
def modify_language():
    stmt = select(Setting).where(Setting.id == 1)
    result = sm.scalars(stmt).first()
    language_arr = config['production'].LANGUAGE
    if request.method == 'POST':
        value = xss_simple(request.form.get('value', ''))
        mark = False
        for r in language_arr:
            if r['key'] == value:
                mark = True
                break
        if not mark:
            return jump(session['lang']['illegal_operation'], url_for('setting.index'))
        try:
            stmt = update(Setting).values(
                value=value
            ).where(Setting.id == 1)
            sm.execute(stmt)
            sm.commit()
            stmt = select(Setting)
            result = sm.scalars(stmt).all()
            dicts = {}
            for r in result:
                dicts.update({r.key: r.value})
            session['setting'] = dicts
            language = session['setting']['language']
            session['lang'] = eval(language)
            return jump(session['lang']['success'], url_for('setting.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('setting/modify_language.html', result=result,language_arr=language_arr)


@setting.route('/modify_logo', methods=['GET', 'POST'])
@admin_required
def modify_logo():
    stmt = select(Setting).where(Setting.id == 4)
    result = sm.scalars(stmt).first()
    if request.method == 'POST':
        value = xss_simple(request.form.get('value', ''))
        try:
            stmt = update(Setting).values(
                value=value
            ).where(Setting.id == 4)
            sm.execute(stmt)
            sm.commit()
            return jump(session['lang']['success'], url_for('setting.index'))
        except Exception as e:
            return str(e)
        finally:
            sm.close()
    return render_template('setting/modify_logo.html', result=result)


@setting.post('/')
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
    msg = 'logo'
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return {
            'code': -2,
            'message': session['lang']['not_select_file']
        }
    if '.' in file.filename:
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext in upload_extension:
            filename = str(time.strftime('%Y%m%d%H%M%S')) + str(random.randint(1000, 9999)) + '.' + ext
            current_dir = os.path.join(upload_dir, msg)
            if not os.path.exists(current_dir) or not os.path.isdir(current_dir):
                os.makedirs(current_dir)
            absolute_filename = os.path.join(current_dir, filename)
            relative_filename = absolute_filename.replace(os.getcwd(), '')
            file.save(absolute_filename)
            compress_image(absolute_filename)
            return {
                'code': 0,
                'message': relative_filename.replace('\\', '/')
            }
        else:
            return {
                'code': -3,
                'message': session['lang']['illegal_files']
            }


def compress_image(file):
    im = cv2.imread(file)
    img_height, img_width = im.shape[:2]
    thumbnail_width = config['production'].LOGO_WIDTH
    thumbnail_height = config['production'].LOGO_HEIGHT
    thumbnail_ratio = config['production'].LOGO_RATIO
    if img_width > thumbnail_width or img_height > thumbnail_height:
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
        im1 = im[y1:y2, x1:x2]
        resized_image = cv2.resize(im1, (thumbnail_width, thumbnail_height), interpolation=cv2.INTER_AREA)
        cv2.imwrite(file, resized_image)
