from flask import Blueprint, request, jsonify
from requests import post, get
from manager.models import AvailableGamesForServers, GameServers, StreamList, GameList, datetime, ClientConnectionList
from manager import db, Config

SERVER_ADDR = 'http://{0}:5000'.format(Config.IP)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "Welcome to the Compal VR Cloud Gaming"


# Register game server
@main.route('/register', methods=['POST'])
def register_game_server():
    games = request.form.getlist('games')
    print(games)
    if games:
        g_server_ip = request.remote_addr
        get_register(g_server_ip)
        print('register game server')
        add_server_games(games, g_server_ip)
        print('add game list')
        return g_server_ip + ' game server registered'

    else:
        return 'Please list available games'


@main.route('/deregister')
def unregister_game_server():
    g_server_ip = request.remote_addr
    print('disconnect ', g_server_ip)
    query = GameServers.query.filter_by(server_ip=g_server_ip).first()

    if query:
        query.is_available = False
        query.client_ip = ''
        delete_games = AvailableGamesForServers.__table__.delete().where(
            AvailableGamesForServers.server_ip == g_server_ip)  # delete the game options in AvailableGamesForServers
        db.session.execute(delete_games)
        db.session.commit()

    return g_server_ip + ' disconnected'


@main.route('/games/<string:game_id>/launch', methods=['GET'])
def playing_game(game_id):
    response = {
        'msg': '',
        'status': False
    }
    player_ip = request.remote_addr
    check_client_status = GameServers.query.filter_by(client_ip=player_ip).first()
    if check_client_status:
        response['msg'] = 'Please close previous game first'
    else:
        # choose game server that has the game installed and is also available
        servers = GameServers.query.\
            join(AvailableGamesForServers,
                 AvailableGamesForServers.server_ip == GameServers.server_ip) \
            .filter(AvailableGamesForServers.game_id == game_id) \
            .filter(GameServers.is_available == True).all()
        print(servers)
        if not servers:  # if cannot query any game server
            response['msg'] = 'Currently no available game server'
        else:
            game_server = servers[0]  # default choose the first object
            game_server_ip = game_server.server_ip
            req_data = {
                # "user_id": user_id,
                "player_ip": player_ip,
                "game_title": game_id,
                "game_id": game_id
            }
            print(game_server_ip)
            game_server_res = post('http://{0}:5000/game-connection'.format(game_server_ip), data=req_data).json()
            print(game_server_res)
            # if game_server_res['launch success']:
            # client's gaming status also needs to update, TBD
            game_server.is_available = False
            game_server.client_ip = player_ip
            db.session.commit()
            # update_waiting_list(player_ip, game_server_ip)

            response['status'] = True
            response['msg'] = 'Connecting... Now launching game title...'
            response['game_server_ip'] = game_server_ip

    resp = jsonify(response)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/resume', methods=['GET'])
def resume_game():
    data = {
        'status': True,
        'server_ip': '',
        'msg': 'Successfully resume the game'
    }
    client_ip = request.remote_addr
    game_connection = ClientConnectionList.query.filter_by(client_ip=client_ip, connection_status='playing').first()
    if game_connection:
        data['server_ip'] = game_connection.server_ip
    else:
        data['status'] = False
        data['msg'] = 'Idle too long... The game has already been closed'
    return data


@main.route('/close', methods=['GET'])
def close_game():
    data = {
        'status': True,
        'msg': 'Successfully close the game'
    }
    client_ip = request.remote_addr
    game_server = GameServers.query.filter_by(client_ip=client_ip, is_available=False).first()
    if game_server:
        req_data = {
            'client_ip': client_ip
        }
        game_server_res = post('http://{0}:5000/game-disconnection'.format(game_server.server_ip), data=req_data).json()
        if not game_server_res['status']:
            data['status'] = False
            data['msg'] = 'Game server error, reset game server now'
        return data

    else:
        data['status'] = False
        data['msg'] = 'Game has been closed'
        return data


@main.route('/connection-status', methods=['POST'])
def update_connection_status():
    print('request update connection: ')
    server_ip = request.remote_addr
    client_ip = request.form.get('client_ip', type=str)
    game_id = request.form.get('game_id', type=str)
    connection_status = request.form.get('connection_status', type=str)
    print(client_ip, game_id, server_ip, connection_status)
    query = ClientConnectionList.query.filter_by(client_ip=client_ip, server_ip=server_ip, game_id=game_id).first()
    if not query:
        print('new connection')
        new_connection = ClientConnectionList(
            server_ip=server_ip,
            client_ip=client_ip,
            # user_id=['client_username'],
            game_id=game_id,
            connection_status=connection_status
        )
        db.session.add(new_connection)
        db.session.commit()
    else:
        update_status(query, connection_status)

    return 'Successfully update status'


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
    db.session.commit()
    return 'table cleaned'


@main.route('/createGame', methods=['POST'])
def add_game():
    new_game = GameList(
        game_id=request.form.get('game_id', type=str),
        game_title=request.form.get('game_title', type=str),
        game_type=request.form.get('game_type', type=str),
        game_brief=request.form.get('game_brief', type=str),
        img_url="{0}/static/games_icon/redout.jpg".format(SERVER_ADDR)
    )
    db.session.add(new_game)
    db.session.commit()
    return {'status': True,
            'msg': 'Successfully add game to the list'}


def get_register(g_server_ip):
    """ register the game server to DB """
    query = GameServers.query.filter_by(server_ip=g_server_ip).first()  # if existed, update its status
    if query:
        query.is_available = True
        query.last_connection_at = datetime.utcnow()
        db.session.commit()
    else:
        new_server = GameServers(server_ip=g_server_ip, last_connection_at=datetime.utcnow())
        db.session.add(new_server)
        db.session.commit()


def register_stream(stream_info):
    new_channel = StreamList(
        server_ip=stream_info['server_ip'],
        client_ip=stream_info['client_ip'],
        client_username=stream_info['client_username'],
        stream_title=stream_info['stream_title'],
        img_url='{0}/static/streams_icon/live_user_chiao622.jpg'.format(SERVER_ADDR),
        stream_url=stream_info['stream_url'],
        started_from=datetime.utcnow())
    db.session.add(new_channel)
    db.session.commit()
    return True


def add_server_games(games, server_ip):
    """ add game options into AvailableGamesForServers """
    game_list = []
    for game_id in games:
        game_list.append(AvailableGamesForServers(game_id=game_id, server_ip=server_ip))

    db.session.add_all(game_list)
    db.session.commit()


def update_status(query, connection_status):
    print('update connection')
    if connection_status == 'playing':
        query.launch_time = datetime.utcnow()
        query.close_time = None
    else:
        query.close_time = datetime.utcnow()
        query.total_play_time = \
            query.total_play_time \
            + (datetime.utcnow() - query.launch_time).total_seconds()
        game_server = GameServers.query.filter_by(client_ip=query.client_ip, is_available=False).first()
        game_server.is_available = True
        game_server.client_ip = ''
    query.connection_status = connection_status
    db.session.commit()
