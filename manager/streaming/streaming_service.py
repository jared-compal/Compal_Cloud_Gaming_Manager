import logging
import datetime

from flask import request, Blueprint

from manager import db
from manager.models import StreamList

streaming_service = Blueprint('streaming_service', __name__)


@streaming_service.route('/')
def test():
    return 'test'


@streaming_service.route('/', methods=['POST'])
def add_stream():
    stream_info = {
        'server_ip': request.form.get('server_ip', type=str),
        'stream_title': request.form.get('stream_title', type=str),
        'client_ip': request.form.get('player_ip', type=str),
        'stream_url': request.form.get('stream_url', type=str),
        'client_username': request.form.get('player_username', type=str)
    }
    if register_stream(stream_info):
        return {'status': True,
                'msg': 'Successfully create streaming channel'}
    return {'status': False,
            'msg': "Couldn't create streaming channel"}


@streaming_service.route('/{stream_id}', methods=['DELETE'])
def delete_stream(stream_id):
    try:
        StreamList.query.filter_by(id=stream_id).delete()
        db.session.commit()
    except Exception as e:
        logging.debug(e)
        return {'msg': 'Error while deleting, try again later...',
                'success': False}

    return {'msg': 'Channel deleted',
            'success': True}


@streaming_service.route('/clean')
def clean_streams():
    StreamList.query.delete()
    db.session.commit()
    return 'table cleaned'


@streaming_service.route('/turn-on')
def turn_on_streaming():
    # 1. check player streaming status
    # 2. check player connection status
    # 3. send request to /obs_start_streaming
    return 'ok'


@streaming_service.route('/turn-off')
def turn_off_streaming():
    # 1. check player streaming status
    # 2. check player connection status
    # 3. send request to /obs_stop_streaming
    return 'ok'


def register_stream(stream_info):
    try:
        new_channel = StreamList(
            server_ip=stream_info['server_ip'],
            client_ip=stream_info['client_ip'],
            client_username=stream_info['client_username'],
            stream_title=stream_info['stream_title'],
            img_url='/static/streams_icon/live_user_chiao622.jpg',
            stream_url=stream_info['stream_url'],
            started_from=datetime.utcnow())
        db.session.add(new_channel)
        db.session.commit()
    except Exception as e:
        logging.debug(e)
        return False
    return True
