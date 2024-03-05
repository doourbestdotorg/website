import os
import random
import time
import cv2
from flask import Blueprint, request, session
from util.util import admin_required, xss_simple
from config.config import config

upload = Blueprint('upload', __name__)


@upload.post('/')
@admin_required
def index():
    upload_dir = config['production'].UPLOAD_DIR
    upload_extension = config['production'].UPLOAD_EXTENSION
    upload_msg = config['production'].UPLOAD_MSG
    if 'file' not in request.files:
        return {
            'code': -1,
            'message': session['lang']['not_select_file']
        }
    file = request.files['file']
    msg = xss_simple(request.form.get('msg'))
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return {
            'code': -2,
            'message': session['lang']['not_select_file']
        }
    if '.' in file.filename and msg in upload_msg:
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext in upload_extension:
            filename = str(time.strftime('%Y%m%d%H%M%S')) + str(random.randint(1000, 9999)) + '.' + ext
            current_dir = os.path.join(upload_dir, msg)
            if not os.path.exists(current_dir) or not os.path.isdir(current_dir):
                os.makedirs(current_dir)
                os.chmod(current_dir, 0o766)
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
    thumbnail_width = config['production'].THUMBNAIL_WIDTH
    thumbnail_height = config['production'].THUMBNAIL_HEIGHT
    thumbnail_ratio = config['production'].THUMBNAIL_RATIO
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
