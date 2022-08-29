from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Role, Account
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # проверяем существует ли такой пользователь
        if not user or not check_password_hash(user.password, password):
            flash('Проверьте свой логин и пароль и попробуйте снова')
            return redirect(url_for('auth.login'))  # перезагрузить страницу

        # если все ок, значит пользователь предоставил правильные логин и пароль
        role_id = user.role_id
        role = Role.query.filter_by(id=role_id).first()

        # если мастер-пользователь, создаем списко всех пользователей по привязанному client_id

        session['users'] = None
        users_list = []
        if role_id == 1:
            users = User.query.filter_by(client_id=user.client_id).all()
            users = [u.name for u in users]
            for u in users:
                users_list.append(u)
            session['users'] = str(users_list)

        # записываем данные из таблицы role в сессию
        session['role_id'] = role_id
        session['role'] = role.name
        session['resources'] = role.resources

        # логин пользователя
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    else:
        return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        client_id = request.form.get('client_id')
        accounts = request.form.get('accounts')
        role_id = request.form.get('role_id')

        # валидация данных
        for value in request.form.values():
            if not value:
                flash('Введите все данные')
                return redirect(url_for('auth.signup'))

        client_id = int(client_id)
        role_id = int(role_id)

        user = User.query.filter_by(email=email).first()  # проверяем есть ли пользователь в БД

        if user:  # если пользователь существует перенеправить на login.html
            flash('Емайл уже существует')
            return redirect(url_for('auth.login'))

        # проверить принадлежат ли аккаунты данному client_id
        accounts_list = [int(account) for account in accounts.split(',')]
        client_accounts = Account.query.filter_by(client_id=client_id).all()
        client_accounts = [account.id for account in client_accounts]
        account_list_diff = list(set(accounts_list) - set(client_accounts))
        if len(account_list_diff) != 0:
            flash(f'Аккаунты {account_list_diff} не принадлежат данному Client ID')
            return redirect(url_for('auth.signup'))

        new_user = User(
            email=email,
            name=name,
            client_id=client_id,
            accounts=accounts,
            role_id=role_id,
            password=generate_password_hash(password, method='sha256')
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    else:
        return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('main.index'))
