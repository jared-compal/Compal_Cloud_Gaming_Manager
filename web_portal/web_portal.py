from flask import Blueprint, render_template

portal = Blueprint('portal', __name__, template_folder='./templates', static_folder='./static')


@portal.route('/')
def portal_page():

    return render_template('./index.html')


@portal.route('/streams/<stream_id>')
def stream_games(stream_id):
    return render_template('./base.html', stream_id=stream_id)


@portal.route('/games/<game_id>')
def portal_games(game_id):

    return render_template('./index.html', game_id=game_id)