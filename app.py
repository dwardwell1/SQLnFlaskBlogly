"""Blogly application."""


from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import *
from datetime import datetime
dt = datetime.today().replace(microsecond=0)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Zipzopper'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def hello():
    return redirect("/users")

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
    img_url = request.form['imgURL']
    img_url = img_url if img_url else None

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>')
def show_user(id):
    user = User.query.get_or_404(id)
    posts = Post.query.filter(Post.user_id == id).all()
    """ Show details about a single user """
    return render_template("myuser.html",user=user, posts=posts)

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
    user.img_url = request.form['imgURL']
    # user.image_url = user.image_url if user.image_url else None
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_user(id):
    """ How to delete by ID """
    user = User.query.filter(User.id == id).delete()
    db.session.commit()
    return redirect('/users')

#posts

@app.route('/users/<int:id>/posts/new')
def new_post_form(id):
    """ new post from """
    user = User.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template("postform.html",user=user, tags=tags)

@app.route('/users/<int:id>/posts/new', methods=["POST"])
def new_post_submit(id):
    """ Submit Post """
    user = User.query.get_or_404(id)
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    """ How did adding an array of tags work in this context? """

    new_post = Post(title=title, content=content, user_id=id, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    
    db.session.commit()
    return redirect(f"/users/{user.id}")
   
@app.route('/posts/<int:id>')
def post(id):
    """ Show post """
    post = Post.query.get_or_404(id)
    
    return render_template("post.html",post=post)



@app.route('/posts/<int:id>/delete', methods=["POST"])
def delete_post(id):
    """ Delete Post"""
    post = Post.query.filter(Post.id == id).first()
    user_id = post.user.id
    post = Post.query.filter(Post.id == id).delete()
   
    db.session.commit()
    return redirect(f'/users/{user_id}')

  
@app.route('/posts/<int:id>/edit')
def edit_post(id):
    """ edit post """
    post = Post.query.get_or_404(id)
    tags = Tag.query.all()

    return render_template("editpost.html",post=post, tags=tags)

@app.route('/posts/<int:id>/edit', methods=["POST"])
def edit_post_submit(id):
    """ submit edit post """
    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.content = request.form['content']
    post.created_at = dt
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags
    

    db.session.commit()
    
    return redirect(f'/posts/{post.id}')

#tags



@app.route('/tags')
def list_tags():
    """ List all tags """
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:id>')
def tag(id):
    """ Show a tags associated posts """
    tag = Tag.query.get_or_404(id)
    return render_template('tag.html', tag=tag)

@app.route('/tags/new')
def new_tag():
    """ Render new tag template """
    return render_template('newtag.html')

@app.route('/tags/new', methods=["POST"])
def tag_submit():
    """ POST new tag """
    tag_name = request.form['name']

    new_tag = Tag(name=tag_name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:id>/edit')
def tag_edit(id):
    """ Edit tag form """
    tag_id = Tag.query.get_or_404(id)

    return render_template('edittag.html', tag= tag_id)

@app.route('/tags/<int:id>/edit', methods=["POST"])
def tag_submit_edit(id):
    """ Submit Tag Edit"""
    tag = Tag.query.get_or_404(id)

    tag.name = request.form['name']

    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):

    # tag = Tag.query.get_or_404(id)
    tag = Tag.query.get_or_404(id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags') 


