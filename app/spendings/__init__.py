from . import routes
from flask import Blueprint

bp = Blueprint('spendings', __name__,
               template_folder='templates', static_folder='static')

bp.secret_key = 'my_secret_key'
