from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user, create_access_token, \
    jwt_required, create_refresh_token, get_current_user

from manager import bcrypt, db
from manager.models import User, Device

auth_service = Blueprint('auth_service', __name__)


@auth_service.route('/device_register', methods=['POST'])
def device_register():
    device_id = request.form.get('device_id', None)
    device_name = request.form.get('device_name', None)
    if device_id and device_name:
        return device_registration(device_id, device_name)
    else:
        return {
            "status": False,
            "msg": "Please provide both device_id and device_name"
        }


@auth_service.route('/device_unregister')
@jwt_required()
def device_unregister():
    delete_device = Device.query.filter_by(id=current_user.id, device_name=current_user.device_name).first()

    db.session.delete(delete_device)
    db.session.commit()
    return jsonify({
                "status": True,
                "msg": "Successfully unregisters device",
                "access_token": None
            })

# @auth_service.route('/user_login', methods=['POST'])
# def user_login():
#     username = request.form.get("username", None)
#     password = request.form.get("password", None)
#     return user_authenticate(username, password)
#
#
# @auth_service.route("/user_logout")
# def user_logout():
#     return jsonify({
#         "status": True,
#         "msg": "Successfully log out user",
#         "access_token": None
#     })
#
#
# @auth_service.route('/user_register', methods=['POST'])
# def user_register():
#     username = request.form.get("username", None)
#     password = request.form.get("password", None)
#     return validate_username(username, password)
#
#
@auth_service.route('/protected')
@jwt_required()
def protected_content():
    return jsonify(
        id=current_user.id,
        username=current_user.username
    )


@auth_service.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    identity = get_current_user()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


def user_authenticate(username, password):
    user = User.query.filter_by(username=username).one_or_none()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        return jsonify({
            "status": True,
            "msg": "Successfully log in user",
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    else:
        return jsonify({
            'status': False,
            'msg': 'Login Unsuccessful. Please check username and password'
        })


def validate_username(username, password):
    msg = "That username is taken. Please choose a different one."
    status = False
    if not User.query.filter_by(username=username).first():
        msg = "Successfully create user"
        status = True
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    return jsonify({
        "status": status,
        "msg": msg
    })


def device_registration(device_id, device_name):
    device = Device.query.filter_by(id=device_id).first()
    print(f"{device_name} register #{device_id}")
    if device is None:
        device = Device(id=device_id, device_name=device_name)
        db.session.add(device)
        db.session.commit()
        access_token = create_access_token(identity=device)
        refresh_token = create_refresh_token(identity=device)
        return jsonify({
            "status": True,
            "msg": f"{device_name} has been assigned as #{device_id}",
            "token": access_token,
            "refresh_token": refresh_token
        })
    else:
        return jsonify({
            'status': False,
            'msg': f'#{device_id} has been taken, please choose another id'
        })
