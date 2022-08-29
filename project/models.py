from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(100))  # имя пользователя (сотрудника компании)
    accounts = db.Column(db.String(100))  #  к каким аккаунтам разрешен доступ
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))
    accounts = db.Column(db.String(100))  # доступ к каким аккаунтам разрешен, например 1,2,3
    resources = db.Column(db.String(100))  # доступ к каким ресурсам разрешен, например, orders, marketing, deliveries


class Client(db.Model):  # таблица компаний-клиентов
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)  # название компании


class Account(db.Model):  # таблица аккаунтов на площадках
    id = db.Column(db.Integer, primary_key=True)
    mp_id = db.Column(db.Integer)  # идентификатор площадки
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
