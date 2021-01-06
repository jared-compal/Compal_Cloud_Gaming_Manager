from flask import Blueprint, request, jsonify
from requests import post, get
from manager.models import GameServers, StreamList, WaitingList, GameList, datetime
from manager import db

SERVER_ADDR = 'http://172.16.0.25:5000'
# SERVER_ADDR = 'http://localhost:5000'
# cloudXR_client_cmd = "C:\Program Files\Nvidia Corporation\CloudXR\Client\CLoudXRClient.exe -w"
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "Welcome to the Compal VR Cloud Gaming"


# Register game server
@main.route('/register')
def register_game_server():
    g_server_ip = request.remote_addr
    print('register', g_server_ip)
    get_register(g_server_ip)
    return g_server_ip + ' game server registered'


# Disconnection signal from game server
@main.route('/deregister')
def unregister_game_server():
    g_server_ip = request.remote_addr
    print('disconnect', g_server_ip)
    query = GameServers.query.filter_by(server_ip=g_server_ip).first()

    if query:
        query.is_available = False
        StreamList.query.filter_by(server_ip=g_server_ip).delete()
        db.session.commit()

    return g_server_ip + ' disconnected'


@main.route('/games/<string:game_id>/launch', methods=['GET'])
def playing_game(game_id):
    response = {
        'msg': '',
        'status': False
    }
    player_ip = request.remote_addr
    is_client_awaiting = WaitingList.query.filter_by(client_ip=player_ip).first()

    if is_client_awaiting:
        processing_server_ip = is_client_awaiting.server_ip
        processing_server_res = get('http://{0}:5000/game-connection'.format(processing_server_ip)).json()
        print(processing_server_res)
        if processing_server_res['status']:
            response['status'] = True
            response['msg'] = 'Successfully launch game server and game title.'
            response['game_server_ip'] = processing_server_ip
            # delete waiting list
            # is_client_awaiting.delete()
            # db.session.commit()
        else:
            response['msg'] = 'Processing... Game server is allocating resources to launch game...'
    else:
        game_server_info = GameServers.query.filter_by(is_available=True).first()
        # If cannot query any game server
        if not game_server_info:
            response['msg'] = 'Currently no available game server'
        else:
            game_server_ip = game_server_info.server_ip
            req_data = {
                "player_ip": player_ip,
                "game_title": game_id,
                "game_id": game_id
            }
            game_server_res = post('http://{0}:5000/game-connection'.format(game_server_ip), data=req_data).json()

            # if game_server_res['launch success']:
            # Client's gaming status also needs to update, TBD
            game_server_info.is_available = False
            db.session.commit()
            # update_waiting_list(player_ip, game_server_ip)
            # save_stream_source(game_server_ip, player_ip, game_id)

            response['status'] = True
            response['msg'] = 'Connecting... Now launching game title...'
            response['game_server_ip'] = game_server_ip
            # else:
            #     response['msg'] = 'Error when launching game server'

    resp = jsonify(response)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/streaming', methods=['POST'])
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
    return {
            'status': False,
            'msg': "Couldn't create streaming channel"
            }


# """
# The following is API for developing or under developing
# """
@main.route('/db')
def db_sync():
    db.create_all()
    return "DB sync"


@main.route('/clean')
def clean_streams():
    StreamList.query.delete()
    WaitingList.query.delete()
    db.session.commit()
    return 'table cleaned'


@main.route('/createGame', methods=['POST'])
def add_game():
    new_game = GameList(
        game_id=request.form.get('game_id', type=int),
        game_title=request.form.get('game_title', type=str),
        game_type=request.form.get('game_type', type=str),
        game_brief=request.form.get('game_brief', type=str),
        img_url="{0}/static/games_icon/redout.jpg".format(SERVER_ADDR)
    )
    db.session.add(new_game)
    db.session.commit()
    return {'status': True,
            'msg': 'Successfully add game to the list'}


# """
# The following is encapsulated functions
# """
def get_register(g_server_ip):
    query = GameServers.query.filter_by(server_ip=g_server_ip).first()
    # If game server registered before, update its is_available and last_connection_at
    if query:
        query.is_available = True
        query.last_connection_at = datetime.utcnow()
        db.session.commit()
    # Create new server entity
    else:
        new_server = GameServers(server_ip=g_server_ip, last_connection_at=datetime.utcnow())
        db.session.add(new_server)
        db.session.commit()


def update_waiting_list(client_ip, server_ip):
    new_client = WaitingList(client_ip=client_ip, server_ip=server_ip)
    db.session.add(new_client)
    db.session.commit()


def register_stream(stream_info):
    new_channel = StreamList(
        server_ip=stream_info['server_ip'],
        client_ip=stream_info['client_ip'],
        client_username=stream_info['client_username'],
        stream_title=stream_info['stream_title'],
        img_url='{0}/static/streams_icon/live_user_lol_ambition.jpg'.format(SERVER_ADDR),
        stream_url=stream_info['stream_url'],
        started_from=datetime.utcnow())
    db.session.add(new_channel)
    db.session.commit()
    return True


