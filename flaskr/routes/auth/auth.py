import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from ...db import get_db
from ...models.user import User

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user = User(
                    username = username,
                    password = generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')

@bp.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.session.query(User).filter_by(username=username).first()
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password,password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')
        
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().session.query(User).filter_by(id=user_id).first()

@bp.route('/logout',methods=['GET','POST'])
def logout():
    # g.pop('user',None)
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auto.login'))
        return view(**kwargs)
    return wrapped_view