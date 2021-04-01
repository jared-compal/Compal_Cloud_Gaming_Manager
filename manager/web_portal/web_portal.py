import logging
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from requests import get
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity,\
    set_access_cookies, unset_jwt_cookies, get_current_user, verify_jwt_in_request
from jwt.exceptions import ExpiredSignatureError

from manager import bcrypt, db, Config
from manager.web_portal.forms import RegistrationForm, LoginForm
from manager.models import User

SERVER_ADDR = Config.SERVER_ADDR
portal = Blueprint('portal', __name__, template_folder='templates', static_folder='static')


@portal.route('/')
def portal_page():
    identity, unset = is_authenticated()
    stream_info = get('{0}/streams'.format(SERVER_ADDR)).json()
    streams = stream_info.get('streams')
    game_info = get('{0}/games'.format(SERVER_ADDR)).json()
    app_info = get('{0}/apps'.format(SERVER_ADDR)).json()
    resp = make_response(render_template(
        'index.html', games=game_info.get('games'), streams=streams,
        apps=app_info.get('apps'), identity=identity
    ))
    if unset:
        unset_jwt_cookies(resp)
    return resp


@portal.route('/games')
def game_page():
    identity, unset = is_authenticated()
    game_info = get('{0}/games'.format(SERVER_ADDR)).json()
    resp = make_response(render_template(
        'category.html', games=game_info.get('games'), title='Game', identity=identity
    ))
    if unset:
        unset_jwt_cookies(resp)
    return resp


@portal.route('/streams')
def stream_page():
    identity, unset = is_authenticated()
    stream_info = get('{0}/streams'.format(SERVER_ADDR)).json()
    resp = make_response(render_template(
        'category.html', streams=stream_info.get('streams'), title='Stream', identity=identity
    ))
    if unset:
        unset_jwt_cookies(resp)
    return resp


@portal.route('/apps')
def app_page():
    identity, unset = is_authenticated()
    app_info = get('{0}/apps'.format(SERVER_ADDR)).json()
    resp = make_response(render_template(
        'category.html', apps=app_info.get('apps'), title='Application', identity=identity
    ))
    if unset:
        unset_jwt_cookies(resp)
    return resp


@portal.route('/popular')
def popular_page():
    identity, unset = is_authenticated()
    game_info = get('{0}/games'.format(SERVER_ADDR)).json()
    app_info = get('{0}/apps'.format(SERVER_ADDR)).json()
    resp = make_response(render_template(
        'category.html', games=game_info.get('games'), apps=app_info.get('apps'), title='Popular', identity=identity
    ))
    if unset:
        unset_jwt_cookies(resp)
    return resp


@portal.route('/streams/<stream_id>')
def portal_streams(stream_id):
    identity, unset = is_authenticated()
    stream_info = get('{0}/streams/{1}'.format(SERVER_ADDR, stream_id)).json()
    if stream_info['status']:
        resp = make_response(render_template(
            'content_page.html', data=stream_info.get('stream'), type='stream', identity=identity
        ))
        if unset:
            unset_jwt_cookies(resp)
        return resp
    return redirect(url_for('portal.portal_page'), code=302)


@portal.route('/games/<game_id>')
def portal_games(game_id):
    identity, unset = is_authenticated()
    game_info = get('{0}/games/{1}'.format(SERVER_ADDR, game_id)).json()
    if game_info['status']:
        resp = make_response(render_template(
            'content_page.html', data=game_info.get('game'), type='game', identity=identity
        ))
        if unset:
            unset_jwt_cookies(resp)
        return resp
    return redirect(url_for('portal.portal_page'), code=302)


@portal.route('/apps/<app_id>')
def portal_apps(app_id):
    identity, unset = is_authenticated()
    app_info = get('{0}/apps/{1}'.format(SERVER_ADDR, app_id)).json()
    if app_info['status']:
        resp = make_response(render_template(
            'content_page.html', data=app_info.get('app'), type='app', identity=identity
        ))
        if unset:
            unset_jwt_cookies(resp)
        return resp
    return redirect(url_for('portal.portal_page'), code=302)


@portal.route("/login", methods=['GET', 'POST'])
def login_page():
    identity, unset = is_authenticated()
    if identity:
        return redirect(url_for('portal.portal_page'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            user = User.query.filter_by(username=username).one_or_none()
            if user and bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity=user)
                resp = redirect(url_for('portal.portal_page'))
                next_page = request.args.get('next')
                if next_page:
                    resp = redirect(next_page)
                set_access_cookies(resp, access_token)
                return resp
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        except Exception as inst:
            logging.debug(inst)
            flash('Internal server error. Please try again later', 'danger')

    resp = make_response(render_template('login.html', title='Login', form=form))
    if unset:

        unset_jwt_cookies(resp)

    return resp


@portal.route('/register', methods=['GET', 'POST'])
def register_page():
    identity, unset = is_authenticated()
    if identity:
        return redirect(url_for('portal.portal_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('portal.login_page'))
    resp = make_response(render_template('register.html', title='Register', form=form))
    if unset:
        unset_jwt_cookies(resp)
    return resp


@portal.route("/logout")
def logout():
    resp = redirect(url_for('portal.login_page'))
    unset_jwt_cookies(resp)
    return resp


# refresh token
@portal.after_request
def refresh_expiring_jwt(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_current_user())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


def is_authenticated():
    unset = False
    try:
        verify_jwt_in_request(optional=True)
        if get_current_user():
            identity = get_current_user()
            return identity, unset
    except ExpiredSignatureError as inst:
        flash('Token expired. Please login again', 'danger')
        print(inst)
        unset = True

    except Exception as inst:
        logging.debug(inst, type(inst))

    return None, unset
