import os
import logging
from flask import Blueprint, request, jsonify, send_from_directory
from requests import post
from flask_login import login_required


from manager.models import AvailableGamesForServers, GameServers, StreamList, \
    GameList, datetime, ClientConnectionList, User, favorite_game_list
from manager import db, Config

SERVER_ADDR = 'http://{0}:5000'.format(Config.IP)
FORMAT = "%(asctime)s -%(levelname)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return "Welcome to the Compal VR Cloud Gaming"


# Register game server
@main.route('/register', methods=['POST'])
def register_game_server():
    games = request.form.getlist('games')
    logging.info('Register game list: ')
    logging.info(games)
    if games:
        g_server_ip = request.remote_addr
        register_server(g_server_ip)
        logging.info('register game server')
        add_server_games(games, g_server_ip)
        logging.info('add game list')
        return {
            'status': True,
            'msg': '{0} game server registered'.format(g_server_ip)
        }
    else:
        return {
            'status': False,
            'msg': 'Please list available games'
        }


@main.route('/deregister')
def unregister_game_server():
    g_server_ip = request.remote_addr
    logging.info('Deregister ' + g_server_ip)
    query = GameServers.query.filter_by(server_ip=g_server_ip).first()

    if query is not None:
        query.is_available = False
        query.client_ip = None
        delete_games = AvailableGamesForServers.__table__.delete().where(
            AvailableGamesForServers.server_ip == g_server_ip)  # delete the game options in AvailableGamesForServers
        db.session.execute(delete_games)
        db.session.commit()
    else:
        return {
            'status': False,
            'msg': "Game server hasn't registered before"
        }

    return {
        'status': True,
        'msg': '{0} deregistered'.format(g_server_ip)
    }


@main.route('/games/<string:game_id>/launch', methods=['GET'])
def playing_game(game_id):
    response = {
        'msg': '',
        'status': False
    }
    player_ip = request.remote_addr
    logging.info(f'Player {player_ip} requests launching game: ')
    check_client_status = GameServers.query.filter_by(client_ip=player_ip).first()
    if check_client_status:
        response['msg'] = 'Please close previous game first'
    else:
        # choose game server that has the game installed and is also available
        servers = GameServers.query\
            .join(AvailableGamesForServers,
                  AvailableGamesForServers.server_ip == GameServers.server_ip) \
            .filter(AvailableGamesForServers.game_id == game_id) \
            .filter(GameServers.is_available == True).all()
        if not servers:  # if cannot query any game server
            response['msg'] = 'Currently no available game server'
        else:
            response['status'] = False
            response['msg'] = 'Selected game is not available'
            game = GameList.query.filter_by(game_id=game_id).first()
            if game is not None:
                response['msg'] = 'Not able to allocate game server at this moment. ' \
                                  'Please play this game later.'
                for game_server in servers:  # loop through game server list and break once game server is available
                    game_server_ip = game_server.server_ip
                    req_data = {
                        # "user_id": user_id,
                        "player_ip": player_ip,
                        "game_title": game.game_title,
                        "game_id": game_id
                    }
                    logging.info('allocate game server: ')
                    logging.info(game_server)
                    logging.info(game_server_ip, req_data)
                    try:
                        game_server_res = post('http://{0}:8080/game-connection'
                                               .format(game_server_ip), data=req_data).json()
                    except Exception as inst:
                        logging.debug('Game server error')
                        logging.debug(inst)
                        game_server.is_available = False
                        db.session.commit()
                    else:
                        if game_server_res['launch success']:
                            game_server.is_available = False
                            game_server.client_ip = player_ip
                            db.session.commit()

                            response['status'] = True
                            response['msg'] = 'Succesfully allocate game server... connecting then launching game title...'
                            response['game_server_ip'] = game_server_ip
                            break

    resp = jsonify(response)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/resume', methods=['GET'])
def resume_game():
    data = {
        'status': True,
        'game_server_ip': '',
        'msg': 'Successfully resume the game'
    }
    client_ip = request.remote_addr
    game_connection = ClientConnectionList.query.filter_by(client_ip=client_ip, connection_status='playing').first()
    logging.info(game_connection)
    if game_connection is not None:
        data['game_server_ip'] = game_connection.server_ip
    else:
        data['status'] = False
        data['msg'] = 'The game has already been closed... it could be due to idling for too long. '
    return data


@main.route('/close', methods=['GET'])
def close_game():
    data = {
        'status': True,
        'msg': 'Successfully close the game'
    }
    client_ip = request.remote_addr
    game_server = GameServers.query.filter_by(client_ip=client_ip, is_available=False).first()
    if game_server is not None:
        req_data = {
            'client_ip': client_ip
        }
        try:
            game_server_res = post('http://{0}:8080/game-disconnection'.format(game_server.server_ip), data=req_data)
        except Exception as e:
            logging.info("Error when closing game")
            logging.debug(e)
            query = ClientConnectionList.query.filter_by(client_ip=client_ip, connection_status='playing').first()
            update_status(query, 'closed')
        else:
            if game_server_res.status_code != 200:
                data['status'] = False
                data['msg'] = 'Game server error, reset game server now'
        return data

    else:
        data['status'] = True
        data['msg'] = 'Game has been closed'
        return data


@main.route('/connection-status', methods=['POST'])
def update_connection_status():

    server_ip = request.remote_addr
    client_ip = request.form.get('client_ip', type=str)
    game_id = request.form.get('game_id', type=str)
    connection_status = request.form.get('connection_status', type=str)
    query = ClientConnectionList.query.filter_by(client_ip=client_ip, server_ip=server_ip, game_id=game_id).first()
    logging.info('Update connection status: ')
    logging.info(f'client ip: {client_ip}, server ip: {server_ip}, game id: {game_id}, status: {connection_status}')
    if query is None:
        logging.info('new connection...')
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
        logging.info('status update - ' + connection_status)
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


@main.route('/download/<filename>')
def download(filename):
    dir_path = os.path.join(main.root_path, 'download')
    return send_from_directory(dir_path, filename, as_attachment=True)


# """
# The following is API for developing or under developing
# """
@main.route('/db')
def db_sync():
    db.create_all()
    # query = GameList.query.filter_by(game_id='410570').first()
    # print(query.users.append(User.query.filter_by(id=2).first()))
    # db.session.commit()
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


def register_server(g_server_ip):
    """ register the game server to DB """
    query = GameServers.query.filter_by(server_ip=g_server_ip).first()  # if existed, update its status
    if query is not None:
        query.is_available = True
        query.last_connection_at = datetime.utcnow()
        query.client_ip = None
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

    if connection_status == 'playing':
        logging.info('playing status update...')
        query.launch_time = datetime.utcnow()
        query.close_time = None
    else:
        logging.info('closed status update...')
        query.close_time = datetime.utcnow()
        query.total_play_time = \
            query.total_play_time \
            + (datetime.utcnow() - query.launch_time).total_seconds()
        game_server = GameServers.query.filter_by(client_ip=query.client_ip, is_available=False).first()
        game_server.is_available = True
        game_server.client_ip = None
    query.connection_status = connection_status
    db.session.commit()
