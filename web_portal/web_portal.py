from flask import Blueprint, render_template
from requests import get


# SERVER_ADDR = 'http://172.16.0.25:5000'
SERVER_ADDR = 'http://localhost:5000'
portal = Blueprint('portal', __name__, template_folder='./templates', static_folder='./static')


@portal.route('/')
def portal_page():
    stream_info = get('{0}/streams'.format(SERVER_ADDR)).json()
    game_info = get('{0}/games'.format(SERVER_ADDR)).json()
    return render_template('./index.html', games=game_info['games'], streams=stream_info['streams'])


@portal.route('/streams/<stream_id>')
def portal_streams(stream_id):
    stream_info = get('{0}/streams/{1}'.format(SERVER_ADDR, stream_id)).json()

    return render_template('./content_page.html', data=stream_info['stream'], type='stream')


@portal.route('/games/<game_id>')
def portal_games(game_id):
    game_info = get('{0}/games/{1}'.format(SERVER_ADDR, game_id)).json()

    return render_template('./content_page.html', data=game_info['game'], type='game')
