from flask import render_template, request, redirect, url_for, flash

from app.db import get_category_db
from app.db import get_spending_db
from . import bp


@bp.route('/create', methods=['GET', 'POST'])
def create_spending():
    if request.method == 'GET':
        categories = get_category_db().get_categories()
        return render_template('spendings/create.html', categories=categories)
    else:
        name = request.form.get('name')
        amount = float(request.form.get('amount'))
        category_id = int(request.form.get('category'))
        date = request.form.get('date')
        is_spending = bool(request.form.get('is_spending'))

        category_name = get_category_db().get_category(category_id)['name']

        get_spending_db().create_spending(name=name, amount=amount, category_id=category_id,
                                          date=date, is_spending=is_spending)

        return redirect('/spendings', code=302)


@bp.route('/')
def get_spendings():
    spendings = get_spending_db().get_spendings()
    spendings_dict = []
    for spending in spendings:
        spendings_dict.append({
            "id": spending['id'],
            "name": spending['name'],
            "amount": spending['amount'],
            "category": get_category_db().get_category(spending['category_id'])['name'],
            "date": spending['date'],
            "is_spending": spending['is_spending']
        })
    return render_template('spendings/index.html', spendings=spendings_dict)


@bp.route('/edit/<int:spending_id>', methods=['GET', 'POST'])
def edit_spending(spending_id):
    spending_db = get_spending_db()
    spending = spending_db.get_spending_by_id(spending_id)

    if request.method == 'POST':
        name = request.form.get('name')
        category_id = request.form.get('category')
        amount = request.form.get('amount')
        is_spending = request.form.get('is_spending')
        date = request.form.get('date')

        get_spending_db().edit_spending(spending_id, name,
                                        category_id, amount, date, is_spending)
        flash('Витрата успішно відредагована', 'success')
        return redirect(url_for('spendings.get_spendings'))

    categories = get_category_db().get_categories()
    return render_template('spendings/edit.html', spending=spending, categories=categories)


@bp.route('/delete/<int:spending_id>', methods=['GET', 'POST'])
def delete_spending(spending_id):
    spending_db = get_spending_db()
    spending_db.delete_spending(spending_id)
    flash('Витрата успішно видалена', 'success')
    return redirect(url_for('spendings.get_spendings'))
