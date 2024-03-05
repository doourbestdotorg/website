import os
import random
import time
from flask import Blueprint, request
from config.config import config
from util.util import admin_required

tinymce = Blueprint('tinymce', __name__)


@tinymce.post('/')
@admin_required
def index():
    upload_dir = config['production'].UPLOAD_DIR
    upload_extension = config['production'].UPLOAD_EXTENSION
    upload_msg = config['production'].UPLOAD_MSG
    tinymce_dir = 'images'
    if 'file' not in request.files:
        return {
            'code': -1,
            'message': 'Please select file'
        }
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    file = request.files['file']
    if file.filename == '':
        return {
            'code': -2,
            'message': 'Please select image'
        }
    if '.' in file.filename:
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext in upload_extension:
            filename = str(time.strftime('%Y%m%d%H%M%S')) + str(random.randint(1000, 9999)) + '.' + ext
            current_dir = os.path.join(upload_dir, tinymce_dir)
            if not os.path.exists(current_dir) or not os.path.isdir(current_dir):
                os.makedirs(current_dir)
            absolute_filename=os.path.join(current_dir, filename)
            relative_filename=absolute_filename.replace(os.getcwd(),'')
            file.save(absolute_filename)
            return {
                "location":relative_filename.replace('\\','/')
            }
        else:
            return {
                'code': -3,
                'message': 'Illegal files'
            }