from flask import render_template, request

from app.db import get_spending_db
from . import bp


@bp.route('/', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        category_id = request.form.get('category')

        spendings = get_spending_db().get_spendings_in_period(
            start_date, end_date, category_id)

        report_data = {
            'title': 'Звіт про витрати',
            'content': 'Це звіт буде вміщувати ваші дані про витрати.',
            'spendings': spendings
        }

        return render_template('categories/report.html', **report_data)

    return render_template('categories/report.html', title='Звіт про витрати',
                           content='Це звіт буде вміщувати ваші дані про витрати.')
