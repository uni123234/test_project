from flask import Flask, g

from app.db import get_db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    with app.app_context():
        get_db(is_server_start=True)

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    from app.categories import bp as categ_bp
    app.register_blueprint(categ_bp, url_prefix='/categories')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    from app.spendings import bp as spending_bp
    app.register_blueprint(spending_bp, url_prefix='/spendings')

    from app.report import bp as report_bp
    app.register_blueprint(report_bp, url_prefix='/report')

    return app
