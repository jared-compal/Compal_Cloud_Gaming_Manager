from flask import Blueprint, request, redirect, url_for, jsonify
from flask_jwt_extended import current_user, create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, get_current_user

from manager import bcrypt
from manager.models import User

auth_service = Blueprint('auth_service', __name__)


@auth_service.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        return user_authenticate(username, password)
    else:
        return {
            'status': False,
            'msg': 'Please login first to access cloud platform resources'
        }


@auth_service.route("/user_logout")
def user_logout():
    resp = jsonify({
        "status": True,
        "msg": "Successfully log out user"
    })
    unset_jwt_cookies(resp)
    return resp


@auth_service.route('/user_register', methods=['POST'])
def user_register():
    return 'Under construction'


@auth_service.route('/protected')
@jwt_required()
def protected_content():
    return jsonify(
        id=current_user.id,
        username=current_user.username
    )


def user_authenticate(username, password):
    user = User.query.filter_by(username=username).one_or_none()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user)
        resp = jsonify({
            "status": True,
            "msg": "Successfully log in user"
        })
        set_access_cookies(resp, access_token)
        print('validate user')
        return resp
    else:
        return jsonify({
            'status': False,
            'msg': 'Login Unsuccessful. Please check username and password'
        })
