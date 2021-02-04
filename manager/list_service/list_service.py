import logging
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_manager, current_user

from manager.models import StreamList, GameList, ClientConnectionList


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


@list_service.route('/favorites')
def favorite_list():
    return 'under construction'


def get_contents(content_type):
    server_ip = 'http://' + current_app.config['IP'] + ':5000'
    data = {
        "status": True,
        content_type: {
        },
        "msg": "Unavailable content type"
    }
    if content_type == 'streams':
        query = StreamList.query.all()
        if query:
            data['total_num'] = len(query)

            for index, item in enumerate(query):
                data[content_type][index] = {
                    "content_id": item.id,
                    "content_title": item.stream_title,
                    "content_brief": item.stream_title,
                    "img_url": server_ip + item.img_url,
                    "content_url": item.stream_url,
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
                    "content_type": item.game_type,
                    "content_brief": item.game_brief,
                    "img_url": server_ip + item.img_url
                }
                data['msg'] = 'Game list...'
            else:
                data['msg'] = 'Currently no available game'
    return data


def get_content(content_type, content_id):
    server_ip = 'http://' + current_app.config['IP'] + ':5000'
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
            data[content_type]["img_url"] = server_ip + item.img_url
            data[content_type]["content_url"] = item.stream_url
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
            data[content_type]["content_type"] = item.game_type
            data[content_type]["content_brief"] = item.game_brief
            data[content_type]["img_url"] = server_ip + item.img_url
        else:
            data["status"] = False
            data["msg"] = "Couldn't find the specific stream"

    return data


def check_user_playing():
    playing_info = ClientConnectionList.query.filter_by(client_ip=request.remote_addr,
                                                        connection_status='playing').first()
    return '' if playing_info is None else playing_info.game_id
