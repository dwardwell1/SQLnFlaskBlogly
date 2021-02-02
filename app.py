"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Zipzopper'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/users')
def list_users():
    """ Show List of all users """
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/users/new')
def create_form():
    return render_template('newform.html')

@app.route('/users/new', methods=['POST'])
def submit_form():
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imgURL']
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>')
def show_user(id):
    user = User.query.get_or_404(id)
    """ Show details about a single pet """
    return render_template("myuser.html",user=user)

@app.route('/users/<int:id>/edit')
def edit_form(id):
    user = User.query.get_or_404(id)
    """ Show form to edit user """
    return render_template("edit.html",user=user)

@app.route('/users/<int:id>/edit', methods=["POST"])
def submit_edit(id):
    user = User.query.get_or_404(id)
    user.first_name = request.form['firstName']
    user.last_name = request.form['lastName']
    user.image_url = request.form['imgURL']
    # user.image_url = user.image_url if user.image_url else None
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:id>/delete', methods=["POST"])
def delete(id):
    """ How to delete by ID """
    user = User.query.filter(User.id == id).delete()
    db.session.commit()
    return redirect('/users')