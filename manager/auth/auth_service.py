from flask import Blueprint

auth_service = Blueprint('auth_service', __name__)


@auth_service.route('/login', methods=['POST'])
def user_login():
    return 'Under construction'


@auth_service.route('/user_register', methods=['POST'])
def user_register():
    return 'Under construction'
