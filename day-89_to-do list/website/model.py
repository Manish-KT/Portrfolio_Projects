from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_heading = db.Column(db.String(100), nullable=False, unique=True)
    task_description = db.Column(db.String(255))
    subtasks = db.relationship('Subtask', backref='task', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subtask_description = db.Column(db.String(255))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    tasks = db.relationship("Task", backref="user", lazy=True)
