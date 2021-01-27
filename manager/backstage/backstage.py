from flask import Blueprint, render_template
from requests import get

from flask_login import login_required

from manager import Config

SERVER_ADDR = 'http://{0}:5000'.format(Config.IP)
backstage = Blueprint('backstage', __name__, template_folder='templates', static_folder='static')


@backstage.route('/')
@login_required
def backstage_home():
    return render_template('backstage_index.html', games=None, streams=None)


@backstage.route('/streams')
@login_required
def backstage_streams():
    stream_info = get('{0}/streams'.format(SERVER_ADDR)).json()
    return render_template('backstage_index.html', streams=stream_info['streams'])


@backstage.route('/games')
@login_required
def backstage_games():
    game_info = get('{0}/games'.format(SERVER_ADDR)).json()
    return render_template('backstage_index.html', games=game_info['games'])
