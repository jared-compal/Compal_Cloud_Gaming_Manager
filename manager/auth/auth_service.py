from flask import Blueprint, request

auth_service = Blueprint('auth_service', __name__)


@auth_service.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        return 'Cannot use login function now'

    else:
        return {
            'status': False,
            'msg': 'Please login first to access cloud platform resources'
        }


@auth_service.route('/user_register', methods=['POST'])
def user_register():
    return 'Under construction'
