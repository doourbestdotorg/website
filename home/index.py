from flask import Blueprint, render_template
from util.util import admin_required

main = Blueprint('index', __name__)


@main.route('/')
@admin_required
def index():
    return render_template('index/index.html')
