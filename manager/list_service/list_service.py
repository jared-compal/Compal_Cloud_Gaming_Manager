import logging
from flask import Blueprint, jsonify, request

from manager import Config
from manager.models import StreamList, GameList, ClientConnectionList, AppList

SERVER_ADDR = 'http://{0}:5000'.format(Config.IP)
list_service = Blueprint('list_service', __name__)


@list_service.route('/streams')
def show_streams():
    try:
        data = get_contents('streams')
        resp = jsonify(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
    except Exception as e:
        logging.debug(e)
        resp = {
            'success': False,
            'msg': 'DB error'
        }

    return resp


@list_service.route('/streams/<string:stream_id>')
def show_stream(stream_id):
    try:
        data = get_content('stream', stream_id)
        resp = jsonify(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
    except Exception as e:
        logging.debug(e)
        resp = {
            'success': False,
            'msg': 'DB error'
        }

    return resp


@list_service.route('/games')
def show_games():
    try:
        data = get_contents('games')
        resp = jsonify(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
    except Exception as e:
        logging.debug(e)
        resp = {
            'success': False,
            'msg': 'DB error'
        }

    return resp


@list_service.route('/games/<string:game_id>')
def show_game(game_id):
    try:
        data = get_content('game', game_id)
        resp = jsonify(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
    except Exception as e:
        logging.debug(e)
        resp = {
            'success': False,
            'msg': 'DB error'
        }

    return resp


@list_service.route('/apps')
def show_apps():
    try:
        data = get_contents('apps')
        resp = jsonify(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
    except Exception as e:
        logging.debug(e)
        resp = {
            'success': False,
            'msg': 'DB error'
        }

    return resp


@list_service.route('/apps/<string:app_id>')
def show_app(app_id):
    try:
        data = get_content('app', app_id)
        resp = jsonify(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
    except Exception as e:
        logging.debug(e)
        resp = {
            'success': False,
            'msg': 'DB error'
        }

    return resp


@list_service.route('/favorites')
def favorite_list():
    return 'under construction'


def get_contents(content_type):
    data = {
        "status": True,
        content_type: {
        },
        "msg": "Unavailable content type"
    }
    if content_type == 'streams':
        query = StreamList.query.order_by(StreamList.id.desc()).all()
        if query:
            data['total_num'] = len(query)

            for index, item in enumerate(query):
                data[content_type][index] = {
                    "content_id": item.id,
                    "content_title": item.stream_title,
                    "content_brief": item.stream_title,
                    "img_url": SERVER_ADDR + item.img_url,
                    "content_url": item.video_source_url,
                    "player_info": item.client_username,
                    "player_id": item.client_username
                }
            data['msg'] = 'Stream list...'
        else:
            data['msg'] = 'Currently no available stream channel'

    if content_type == 'games':
        query = GameList.query.all()
        playing_game_id = check_user_playing()
        if query:
            data['total_num'] = len(query)
            for index, item in enumerate(query):
                launched = False
                if playing_game_id == item.game_id:
                    launched = True
                data[content_type][index] = {
                    "already_launched": launched,
                    "content_id": item.game_id,
                    "content_title": item.game_title,
                    "content_type": item.game_genre,
                    "content_brief": item.game_brief,
                    "img_url": SERVER_ADDR + item.img_url
                }
                data['msg'] = 'Game list...'
            else:
                data['msg'] = 'Currently no available game'

    if content_type == 'apps':
        query = AppList.query.all()
        playing_game_id = check_user_playing()
        if query:
            data['total_num'] = len(query)
            for index, item in enumerate(query):
                launched = False
                if playing_game_id == item.app_id:
                    launched = True
                data[content_type][index] = {
                    "already_launched": launched,
                    "content_id": item.app_id,
                    "content_title": item.app_title,
                    "content_type": item.app_genre,
                    "content_brief": item.app_brief,
                    "img_url": SERVER_ADDR + item.img_url
                }
                data['msg'] = 'App list...'
            else:
                data['msg'] = 'Currently no available app'

    return data


def get_content(content_type, content_id):
    data = {
        "status": True,
        content_type: {
        }
    }
    if content_type == 'stream':
        item = StreamList.query.filter_by(id=content_id).first()
        if item:
            data[content_type]["content_id"] = item.id
            data[content_type]["content_title"] = item.stream_title
            data[content_type]["content_brief"] = item.stream_title
            data[content_type]["img_url"] = SERVER_ADDR + item.img_url
            data[content_type]["content_url"] = item.video_source_url
            data[content_type]["player_info"] = item.client_username
            data[content_type]["player_id"] = item.client_username
        else:
            data["status"] = False
            data["msg"] = "Couldn't find the specific stream"

    if content_type == 'game':
        item = GameList.query.filter_by(game_id=content_id).first()
        playing_game_id = check_user_playing()
        launched = False
        if playing_game_id == content_id:
            launched = True
        if item:
            data[content_type]["already_launched"] = launched
            data[content_type]["content_id"] = item.game_id
            data[content_type]["content_title"] = item.game_title
            data[content_type]["content_type"] = item.game_genre
            data[content_type]["content_brief"] = item.game_brief
            data[content_type]["img_url"] = SERVER_ADDR + item.img_url
        else:
            data["status"] = False
            data["msg"] = "Couldn't find the specific game"

    if content_type == 'app':
        item = AppList.query.filter_by(app_id=content_id).first()
        playing_game_id = check_user_playing()
        launched = False
        if playing_game_id == content_id:
            launched = True
        if item:
            data[content_type]["already_launched"] = launched
            data[content_type]["content_id"] = item.app_id
            data[content_type]["content_title"] = item.app_title
            data[content_type]["content_type"] = item.app_genre
            data[content_type]["content_brief"] = item.app_brief
            data[content_type]["img_url"] = SERVER_ADDR + item.img_url
        else:
            data["status"] = False
            data["msg"] = "Couldn't find the specific app"

    return data


def check_user_playing():
    client_ip = request.args.get('id')
    if client_ip is None:
        client_ip = request.remote_addr
    playing_info = ClientConnectionList.query.filter_by(client_ip=client_ip,
                                                        connection_status='playing').first()
    return '' if playing_info is None else playing_info.app_id
