from flask import Blueprint, request, redirect, url_for
from flask_login import login_user, current_user, logout_user

from manager import bcrypt, db
from manager.models import User

auth_service = Blueprint('auth_service', __name__)


@auth_service.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            if request.form.get('remember'):
                login_user(user, remember=request.form.get('remember'))
            else:
                login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            return {'status': False,
                    'msg': 'Login Unsuccessful. Please check username and password'
                    }
    else:
        return {'status': False,
                'msg': 'Please login first to access cloud platform resources'
                }


@auth_service.route("/user_logout")
def user_logout():
    logout_user()
    return redirect(url_for('auth_service.user_login'))


@auth_service.route('/user_register', methods=['POST'])
def user_register():
    return 'Under construction'
