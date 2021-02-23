import logging

from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from requests import get
from flask_jwt_extended import jwt_required, get_jwt, create_access_token, \
    set_access_cookies, unset_jwt_cookies, get_current_user, verify_jwt_in_request

from manager import bcrypt, db, Config
from manager.web_portal.forms import RegistrationForm, LoginForm
from manager.models import User

SERVER_ADDR = Config.SERVER_ADDR
portal = Blueprint('portal', __name__, template_folder='templates', static_folder='static')


@portal.route('/')
def portal_page():
    identity, unset = is_authenticated()
    stream_info = get('{0}/streams'.format(SERVER_ADDR)).json()
    game_info = get('{0}/games'.format(SERVER_ADDR)).json()
    resp = make_response(render_template(
        'index.html', games=game_info.get('games'), streams=stream_info.get('streams'), identity=identity
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


def is_authenticated():
    unset = False
    try:
        verify_jwt_in_request(optional=True)
        if get_current_user():
            identity = get_current_user()
            print(identity.username, identity.roles[0].name)
            return identity, unset
    except Exception as inst:
        print(inst)
        unset = True
    return None, unset
