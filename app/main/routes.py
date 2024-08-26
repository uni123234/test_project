from flask import render_template

from . import bp


@bp.route('/')
def get_index():
    return render_template('categories/start.html')
