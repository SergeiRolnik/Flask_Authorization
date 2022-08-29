from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user
from .models import User, Role

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


# пример страницы только для мастер-пользователей
@main.route('/master')
@login_required
def master():
    if current_user.role_id == 1:
        role = Role.query.filter_by(id=current_user.role_id).first()
        context = {
                    'current_user': current_user.name,
                    'current_user_role': role.name,
                    'client_id': current_user.client_id,
                    'accounts': current_user.accounts,
                    'users': session['users']
        }
        return render_template('master.html', context=context)
    else:
        return redirect(url_for('main.index'))


@main.route('/profile')
@login_required
def profile():
    context = {
        'current_user': current_user.name,
        'current_user_email': current_user.email,
        'current_user_role': session['role'],
        'current_user_resources': session['resources'],
        'current_user_accounts': current_user.accounts
    }
    return render_template('profile.html', context=context)


@main.route('/marketing')
@login_required
def marketing():
    role = Role.query.filter_by(id=current_user.role_id).first()
    if 'marketing' in role.resources:
        context = {'current_user': current_user.name, 'current_user_role': role.name}
        return render_template('marketing.html', context=context)
    else:
        return redirect(url_for('main.index'))


@main.route('/orders')
@login_required
def orders():
    role = Role.query.filter_by(id=current_user.role_id).first()
    if 'orders' in role.resources:
        context = {'current_user': current_user.name, 'current_user_role': role.name}
        return render_template('orders.html', context=context)
    else:
        return redirect(url_for('main.index'))


@main.route('/stocks')
@login_required
def stocks():
    role = Role.query.filter_by(id=current_user.role_id).first()
    if 'stocks' in role.resources:
        context = {'current_user': current_user.name, 'current_user_role': role.name}
        return render_template('stocks.html', context=context)
    else:
        return redirect(url_for('main.index'))
