from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from requests import get
from flask_login import login_user, current_user, logout_user, login_required

from manager import bcrypt, db
from manager.web_portal.forms import RegistrationForm, LoginForm
from manager.models import User

portal = Blueprint('portal', __name__, template_folder='templates', static_folder='static')


@portal.route('/')
def portal_page():
    server_address = 'http://{0}:5000'.format(current_app.config['IP'])
    stream_info = get('{0}/streams'.format(server_address)).json()
    game_info = get('{0}/games'.format(server_address)).json()
    return render_template('index_test.html', games=game_info.get('games'), streams=stream_info.get('streams'))


@portal.route('/streams/<stream_id>')
def portal_streams(stream_id):
    server_address = 'http://{0}:5000'.format(current_app.config['IP'])
    stream_info = get('{0}/streams/{1}'.format(server_address, stream_id)).json()
    if stream_info['status']:
        return render_template('content_page_test.html', data=stream_info.get('stream'), type='stream')
    return redirect(url_for('portal.portal_page'), code=302)


@portal.route('/games/<game_id>')
def portal_games(game_id):
    server_address = 'http://{0}:5000'.format(current_app.config['IP'])
    game_info = get('{0}/games/{1}'.format(server_address, game_id)).json()
    if game_info['status']:
        return render_template('content_page_test.html', data=game_info.get('game'), type='game')
    return redirect(url_for('portal.portal_page'), code=302)


@portal.route("/login", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('portal.portal_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('portal.portal_page'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@portal.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('portal.login_page'))
    return render_template('register.html', title='Register', form=form)


@portal.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('portal.portal_page'))


# @portal.route("/account")
# @login_required
# def account():
#     return render_template('account.html', title='Account')
