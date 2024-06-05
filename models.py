from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    properties = db.relationship('PlayerProperties', backref='user', lazy=True, uselist=False)

class PlayerProperties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.Integer, nullable=False, default=0)
    if_chef_orders = db.Column(db.Integer, nullable=False, default=0)
    if_waiter_orders = db.Column(db.Integer, nullable=False, default=0)
    for_chef_orders = db.Column(db.Integer, nullable=False, default=0)
    for_waiter_orders = db.Column(db.Integer, nullable=False, default=0)
    put_chef_orders = db.Column(db.Integer, nullable=False, default=0)
    put_waiter_orders = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
