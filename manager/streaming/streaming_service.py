import logging

from flask import request, Blueprint
from requests import get

from manager import db
from manager.models import StreamList, ClientConnectionList, datetime, GameList

streaming_service = Blueprint('streaming_service', __name__)


@streaming_service.route('/', methods=['POST'])  # API for game server to update
def add_stream():
    try:
        client_ip = request.form.get('client_ip', type=str)
        connection = ClientConnectionList.query.filter_by(client_ip=client_ip).first()
        game_id = connection.game_id
        game = GameList.query.filter_by(game_id=game_id).first()
        video_source_url = 'http://' + request.remote_addr + request.form.get('video_source_url', type=str)
        stream_info = {
            'server_ip': request.form.get('game_server_ip', type=str),
            # 'stream_title': request.form.get('stream_title', type=str),
            'stream_title': game.game_title,
            'client_ip': client_ip,
            'stream_url': video_source_url,
            'video_source_url': video_source_url,
            # 'client_username': request.form.get('player_username', type=str)
            'client_username': 'Compal'
        }
        stream_id = register_stream(stream_info)
        if stream_id:
            return {'status': True,
                    'msg': 'Successfully create streaming channel',
                    'stream_id': stream_id}
    except Exception as inst:
        logging.debug(inst)

    return {'status': False,
            'msg': "Couldn't create streaming channel"}


@streaming_service.route('/<string:stream_id>', methods=['DELETE'])  # API for game server to update
def delete_stream(stream_id):
    print(stream_id)
    try:
        StreamList.query.filter_by(id=stream_id).delete()
        db.session.commit()
    except Exception as e:
        logging.debug(e)
        return {'msg': 'Error while deleting, try again later...',
                'success': False}

    return {'msg': 'Channel deleted',
            'success': True}


@streaming_service.route('/start')  # API for front-end client
def start_streaming():
    # client_ip = request.remote_addr
    client_ip = request.args.get('client')
    connection = ClientConnectionList.query.filter_by(client_ip=client_ip).first()

    if connection.connection_status == 'playing':
        game_server_ip = connection.server_ip

        # 3. send request to /obs_start_streaming
        try:
            server_resp_json = get('http://{0}:8080/obs_start_streaming?client_ip={1}'
                                   .format(game_server_ip, client_ip), timeout=30)
            server_resp = server_resp_json.json()
        except Exception as e:
            logging.debug(e)
            return {
                'status': True,
                'msg': 'Something went wrong...',
            }

        if server_resp['status']:
            return {
                'status': True,
                'msg': 'Launching streaming channel now...',
            }

    return {
        'status': False,
        'msg': 'Error when launching streaming channel... please make sure to launch game title first'
    }


@streaming_service.route('/stop')  # API for front-end client
def stop_streaming():
    # client_ip = request.remote_addr
    client_ip = request.args.get('client')
    streaming_channel = StreamList.query.filter_by(client_ip=client_ip).first()
    if streaming_channel:
        game_server_ip = streaming_channel.server_ip
        server_resp_json = get('http://{0}:8080/obs_stop_streaming?client_ip={1}'
                               .format(game_server_ip, client_ip))
        server_resp = server_resp_json.json()
        if server_resp['status']:
            return {
                'status': True,
                'msg': 'Stop streaming channel now...',
            }
    else:
        return {
            'status': True,
            'msg': 'Streaming channel has already stopped...',
        }
    return {
        'status': False,
        'msg': 'Error when stop streaming channel... please send the request later'
    }


@streaming_service.route('/clean')
def clean_streams():
    StreamList.query.delete()
    db.session.commit()
    return 'table cleaned'


def register_stream(stream_info):
    try:
        new_channel = StreamList(
            server_ip=stream_info['server_ip'],
            client_ip=stream_info['client_ip'],
            client_username=stream_info['client_username'],
            stream_title=stream_info['stream_title'],
            img_url='/static/streams_icon/live_user_chiao622.jpg',
            stream_url=stream_info['stream_url'],
            video_source_url=stream_info['video_source_url'],
            started_from=datetime.utcnow())
        db.session.add(new_channel)
        db.session.commit()
        return new_channel.id
    except Exception as e:
        logging.debug(e)
        return None
