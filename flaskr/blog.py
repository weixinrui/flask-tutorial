from flask import (
    Blueprint, flash, g, redirect, url_for, render_template, request
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from .models import User
from .models import Post

bp = Blueprint('blog',__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.session.query(Post).all()
    return render_template('blog/index.html',posts=posts)

@bp.route('/create',methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            post = Post(
                title = title,
                body = body,
                author_id = g.user.id
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_post(id,check_author=True):
    post = get_db().session.query(Post).filter(id == id).first()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)
    return post

@bp.route('/<int:id>/update',methods=['GET','POST'])
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            post = db.session.query(Post).filter(id == id).first()
            if post:
                post.title = title
                post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html',post=post)

@bp.route('/<int:id>/delete',methods=['GET','POST'])
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    post = db.session.query(Post).filter(id == id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('blog.index'))