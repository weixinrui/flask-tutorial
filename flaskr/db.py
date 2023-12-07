import click
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db():
    return db

def close_db(e=None):
    db = g.pop('db',None)
    
    if db is not None:
        db.close()

def init_db(app):
    from .models import User
    from .models import Post
    with app.app_context():
        db.create_all()
    
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db(current_app)
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskr.sqlite"
    db.init_app(app)