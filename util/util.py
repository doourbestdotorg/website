import datetime
import functools
import hashlib
import random
import string
import time
import bleach
from bleach.css_sanitizer import CSSSanitizer
from flask import redirect, url_for, session
from sqlalchemy import select

from db.Admin import Admin
from db.Base import sm


# filter rich text
def xss_rich(strs):
    css_sanitizers = CSSSanitizer(
        allowed_css_properties=['color', 'font-weight', 'display', 'float', 'text-align', 'background-color', 'float'])
    attrs = {
        '*': ['class', 'style'],
        'a': ['href', 'rel', 'title'],
        'img': ['alt', 'src'],
    }
    result = bleach.clean(
        strs,
        tags={'p', 'a', 'strong', 'img', 'video', 'ul', 'li', 'span', 'em'},
        attributes=attrs,
        css_sanitizer=css_sanitizers
    )
    return result


# filter simple text
def xss_simple(strs):
    return bleach.clean(strs)


# jump to specified page
def jump(message='', jump_url='', last_time=3):
    return redirect(url_for('jump', message=message, jump_url=jump_url, last_time=last_time))


def get_hash256(my_str):
    hash_str = hashlib.sha256()
    hash_str.update(my_str.encode('utf-8'))
    last_str = hash_str.hexdigest()
    return last_str


# generated random string
def get_salt(length=8):
    char = string.ascii_letters + string.digits
    return "".join(random.choice(char) for _ in range(length))


# datetime to timestamp
def date_to_time(date_str):
    # date_str = "2016-05-05 20:28:54"
    time_array = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # Convert to timestamp
    timestamp = time.mktime(time_array)
    return round(timestamp)


# current datetime
def get_date_number():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


# timestamp to datetime
def time_to_datetime(time_number):
    time_number = int(time_number)
    x = time.localtime(time_number)
    return time.strftime('%Y-%m-%d %H:%M:%S', x)


# verify permission
def admin_required(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if 'username' in session and 'shell' in session and 'token' in session:
            stmt = select(Admin).where(Admin.username == xss_simple(session['username']))
            result = sm.scalars(stmt).first()
            if session['shell'] == get_hash256(str(session['username']) + get_hash256(session['token']) + result.salt):
                return func(*args, **kwargs)
        return redirect(url_for('login.index'))
    return inner
