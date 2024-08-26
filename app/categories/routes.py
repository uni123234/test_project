from flask import render_template, request, redirect, abort

from app.categories import bp
from app.db import get_category_db


@bp.route('/')
def get_categories():
    categories = get_category_db().get_categories()
    categories_dict = []
    for category in categories:
        categories_dict.append({
            "id": category[0],
            "name": category[1],
            "description": category[2],
            "color": category[3],
        })
    return render_template('categories/index.html', categories=categories_dict)


@bp.route('/create', methods=['GET', 'POST'])
def create_category():
    if request.method == 'GET':
        return render_template('categories/create.html')
    else:
        name = request.form.get('name')
        description = request.form.get('description')
        color = request.form.get('color')
        db = get_category_db()

        db.create_category(name=name, description=description, color=color)
        return redirect('/categories', code=302)


@bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    db = get_category_db()
    if request.method == 'GET':
        category = db.get_category(id=category_id)
        if category:
            print(category)
            return render_template('categories/edit.html', name=category[0], description=category[1], color=category[2])
        abort(404)
    else:
        name = request.form.get('name')
        description = request.form.get('description')
        color = request.form.get('color')

        db.edit_category(id=category_id, name=name,
                         description=description, color=color)
        return redirect('/categories', code=302)


@bp.route('/delete/<int:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):
    db = get_category_db()
    if request.method == 'GET':
        category = db.get_category(id=category_id)
        if category:
            return render_template('categories/delete.html', name=category[0], description=category[1],
                                   color=category[2])
        abort(404)
    else:
        db.delete_category(id=category_id)
        return redirect('/categories', code=302)
