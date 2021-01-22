from flask import Blueprint, jsonify, request
from flask_login import login_manager, current_user

from manager.models import StreamList, GameList, ClientConnectionList

list_service = Blueprint('list_service', __name__)


@list_service.route('/streams')
def show_streams():
    query = StreamList.query.all()
    data = {
        "status": True,
        "streams": {
        }
    }
    if query:
        data['total_num'] = len(query)

        i = 0
        for item in query:
            data['streams'][i] = {
                "content_id": item.id,
                "content_title": item.stream_title,
                "content_brief": item.stream_title,
                "img_url": item.img_url,
                "content_url": item.stream_url,
                "player_info": item.client_username,
                "player_id": item.client_username
            }
            i += 1
    else:
        data['status'] = False
        data['msg'] = 'Currently no available stream channel'

    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@list_service.route('/streams/<string:stream_id>')
def show_stream(stream_id):
    item = StreamList.query.filter_by(id=stream_id).first()
    if item:
        data = {
            "status": True,
            "stream": {
                "content_id": item.id,
                "content_title": item.stream_title,
                "content_brief": item.stream_title,
                "img_url": item.img_url,
                "content_url": item.stream_url,
                "player_info": item.client_username
            }
        }
    else:
        data = {
            "status": False,
            "msg": "Couldn't find the specific stream channel"
        }

    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@list_service.route('/games')
def show_games():
    query = GameList.query.all()
    playing = ClientConnectionList.query.filter_by(client_ip=request.remote_addr,
                                                   connection_status='playing').first()
    playing_game_id = ''
    if playing is not None:
        print('playing yes')
        playing_game_id = playing.game_id
    data = {
            "status": True,
            "games": {
            }}
    if query:
        data['total_num'] = len(query)
        i = 0
        for item in query:
            launched = False
            if playing_game_id == item.game_id:
                launched = True
            data['games'][i] = {
                "already_launched": launched,
                "content_id": item.game_id,
                "content_title": item.game_title,
                "content_type": item.game_type,
                "content_brief": item.game_brief,
                "img_url": item.img_url
            }
            i += 1
    else:
        data['status'] = False
        data['msg'] = 'Currently no available game'

    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@list_service.route('/games/<string:game_id>')
def show_game(game_id):
    item = GameList.query.filter_by(game_id=game_id).first()
    playing = ClientConnectionList.query.filter_by(game_id=game_id, client_ip=request.remote_addr,
                                                   connection_status='playing').first()
    playing_game_id = ''
    if playing is not None:
        playing_game_id = playing.game_id
    launched = False
    print(playing_game_id, game_id)
    if playing_game_id == game_id:
        launched = True
    if item is not None:
        data = {
            "status": True,
            'game': {
                "already_launched": launched,
                "content_id": item.game_id,
                "content_title": item.game_title,
                "content_type": item.game_type,
                "content_brief": item.game_brief,
                "img_url": item.img_url
            }
        }
    else:
        data = {
            "status": False,
            "msg": "Couldn't find the specific game"
        }

    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
