import datetime

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from . import db
from .models import Note, Category, User
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        due_date = request.form.get('due-date')
        category_name = request.form.get('category')
        category = Category.query.filter_by(name=category_name).first()

        if len(note) < 1:
            flash('Note is too short!', category='error')
        if not category_name:
            flash('You have to select a category.', category='error')
        else:
            new_note = Note(data=note, due_date=due_date, user_id=current_user.id, category_id=category.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    user = User.query.filter_by(id=current_user.id).first()
    notes = Note.query.filter_by(user_id=current_user.id).order_by(desc(Note.date)).all()
    category_names = {category.id: category.name for category in Category.query.all()}
    return render_template("home.html", user=user, notes=notes, category_names=category_names)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/update-note', methods=['POST'])
def update_note():
    pass


@views.route('/add-category', methods=['POST', 'GET'])
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category')
        category = Category.query.filter_by(name=category_name).first()

        if category:
            flash('Category already exists.', category='error')
        elif len(category_name) < 1:
            flash('Category title is too short!', category='error')
        else:
            new_category = Category(name=category_name, user_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
            flash('Category added!', category='success')

    return render_template('categories.html', user=current_user)


@views.route('/delete-category', methods=['POST'])
def delete_category():
    category = json.loads(request.data)
    category_id = category['categoryId']
    category = Category.query.get(category_id)
    if category:
        if category.user_id == current_user.id:
            db.session.delete(category)
            db.session.commit()

    return jsonify({})

