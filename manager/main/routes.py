import os
import logging
from flask import Blueprint, request, jsonify, send_from_directory
from requests import post, get
from flask_jwt_extended import jwt_required, current_user

from manager.models import GameServers, \
    GameList, datetime, ClientConnectionList, User, Role, \
    AvailableAppsForServers, AppList, StreamList
from manager import db, Config

SERVER_ADDR = Config.SERVER_ADDR
FORMAT = "%(asctime)s -%(levelname)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "Welcome to the Compal VR Cloud Gaming"


# Register game server
@main.route('/register', methods=['POST'])
def register_game_server():
    apps = request.form.getlist('apps')
    logging.info('Register game list: ')
    logging.info(apps)
    if apps:
        g_server_ip = request.remote_addr
        register_server(g_server_ip)
        logging.info('register game server')
        add_server_games(apps, g_server_ip)
        logging.info('add app list')
        return {
            'status': True,
            'msg': '{0} edge server registered'.format(g_server_ip)
        }
    else:
        return {
            'status': False,
            'msg': 'Please list available apps'
        }


@main.route('/deregister')
def unregister_game_server():
    g_server_ip = request.remote_addr
    logging.info('Deregister ' + g_server_ip)
    query = GameServers.query.filter_by(server_ip=g_server_ip).first()

    if query is not None:
        query.is_available = False
        query.client_ip = None
        # delete_games = AvailableGamesForServers.__table__.delete().where(
        #     AvailableGamesForServers.server_ip == g_server_ip)  # delete the game options in AvailableGamesForServers
        delete_apps = AvailableAppsForServers.__table__.delete().where(
            AvailableAppsForServers.server_ip == g_server_ip)  # delete the app options in AvailableGamesForServers

        # db.session.execute(delete_games)
        db.session.execute(delete_apps)
        db.session.commit()
    else:
        return {
            'status': False,
            'msg': "Edge server hasn't registered before"
        }

    return {
        'status': True,
        'msg': '{0} deregistered'.format(g_server_ip)
    }


@main.route('/games/<string:game_id>/launch', methods=['GET'])
def playing_game(game_id):
    logging.info('launch game')
    response = {
        'msg': '',
        'status': False
    }

    # client_ip = request.args.get('id')
    client_ip = current_user.id
    print('client_id: ', client_ip)
    if client_ip is None:
        client_ip = request.remote_addr

    logging.info(f'Client {client_ip} requests launching game: ')
    query = GameList.query.filter_by(game_id=game_id).first()
    if query:
        response = launch_app(response, client_ip, game_id, query.game_title, query.platform)
    else:
        response['msg'] = 'Selected game is not available'
    resp = jsonify(response)
    logging.info(response)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/apps/<string:app_id>/launch', methods=['GET'])
def playing_app(app_id):
    logging.info('launch app')
    response = {
        'msg': '',
        'status': False
    }
    client_ip = request.args.get('id')
    if client_ip is None:
        client_ip = request.remote_addr
    logging.info(f'Client {client_ip} requests launching app: ')
    query = AppList.query.filter_by(app_id=app_id).first()
    if query:
        response = launch_app(response, client_ip, app_id, query.app_title, query.platform)
    else:
        response['msg'] = 'Selected app is not available'
    resp = jsonify(response)
    logging.info(response)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/resume', methods=['GET'])
def resume_game():
    data = {
        'status': True,
        'game_server_ip': '',
        'msg': 'Successfully resume the app'
    }
    client_ip = request.args.get('id')
    if client_ip is None:
        client_ip = request.remote_addr

    game_connection = ClientConnectionList.query.filter_by(client_ip=client_ip, connection_status='playing').first()
    if game_connection is not None:
        data['game_server_ip'] = game_connection.server_ip
    else:
        data['status'] = False
        data['msg'] = 'The app has already been closed... it could be due to idling for too long. '
    return data


@main.route('/close', methods=['GET'])
def close_game():
    logging.info('closed request')
    data = {
        'status': True,
        'msg': 'Successfully close the app'
    }
    client_ip = request.args.get('id')
    if client_ip is None:
        client_ip = request.remote_addr
    game_server = GameServers.query.filter_by(client_ip=client_ip, is_available=False).first()
    if game_server is not None:
        req_data = {
            'client_ip': client_ip
        }
        try:
            print('http://{0}:8080/game-disconnection'.format(game_server.server_ip))
            game_server_res = post('http://{0}:8080/game-disconnection'.format(game_server.server_ip), data=req_data)
        except Exception as e:
            logging.info("Error when closing app")
            logging.debug(e)
            query = ClientConnectionList.query.filter_by(client_ip=client_ip, connection_status='playing').first()
            update_status(query, 'closed')
        else:
            if game_server_res.status_code != 200:
                data['status'] = False
                data['msg'] = 'Edge server error, reset edge server now'
        return data

    else:
        data['status'] = True
        data['msg'] = 'App is closing...'
        return data


@main.route('/connection-status', methods=['POST'])
def update_connection_status():
    server_ip = request.remote_addr
    client_ip = request.form.get('client_ip', type=str)
    app_id = request.form.get('app_id', type=str)
    connection_status = request.form.get('connection_status', type=str)
    platform = request.form.get('platform', type=str)
    query = ClientConnectionList.query.filter_by(client_ip=client_ip, server_ip=server_ip,
                                                 app_id=app_id, platform=platform).first()
    logging.info('Update connection status: ')
    logging.info(f'client ip: {client_ip}, server ip: {server_ip},'
                 f'app id: {app_id}, platform: {platform}, status: {connection_status}')

    if connection_status == 'timeout':
        register_server(server_ip)
        return 'Client connection timeout... '

    if query is None:
        logging.info('new connection...')
        new_connection = ClientConnectionList(
            server_ip=server_ip,
            client_ip=client_ip,
            # user_id=['client_username'],
            app_id=app_id,
            platform=platform,
            connection_status=connection_status
        )
        db.session.add(new_connection)
        db.session.commit()

    else:
        logging.info('status update - ' + connection_status)
        update_status(query, connection_status)

    # Temporary method to open stream
    if connection_status == "playing":
        try:
            start_streaming_res = get('{0}/streaming/start?client_ip={1}'.format(SERVER_ADDR, client_ip)).json()
            if not start_streaming_res['status']:
                return 'Successfully update status but fail to open streaming'
        except Exception as inst:
            logging.debug(inst)

    return 'Successfully update status'


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
    db.session.commit()

    return "DB sync"


@main.route('/createGame', methods=['POST'])
def create_game():
    new_game = GameList(
        game_id=request.form.get('game_id', type=str),
        game_title=request.form.get('game_title', type=str),
        game_genre=request.form.get('game_genre', type=str),
        game_brief=request.form.get('game_brief', type=str),
        img_url="{0}/static/games_icon/redout.jpg".format(SERVER_ADDR)
    )
    db.session.add(new_game)
    db.session.commit()
    return {'status': True,
            'msg': 'Successfully add game to the list'}


# """
# The following is utility function
# """
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


def add_server_games(apps, server_ip):
    """ add game options into AvailableGamesForServers """
    app_list = []
    for app in apps:
        app_list.append(AvailableAppsForServers(app_id=app, server_ip=server_ip))

    db.session.add_all(app_list)
    db.session.commit()


def update_status(query, connection_status):
    """ update the connection status between game server and player """
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
        try:
            StreamList.query.filter_by(server_ip=game_server.server_ip).delete()
        except Exception as e:
            logging.debug(e)
    query.connection_status = connection_status
    db.session.commit()
    return


def launch_error_handling(check_client_status):
    error_server_ip = check_client_status.server_ip
    try:
        check_client_status.is_available = True
        # check_client_status.is_available = False
        check_client_status.client_ip = None
        db.session.commit()
        res = get('http://{0}:8080/connection-timeout'.format(error_server_ip), timeout=5)
        logging.debug(res)
    except Exception as e:
        logging.debug(e)
        logging.debug('Game server no response... not available...')


def launch_app(response, player_ip, app_id, app_title, platform):
    check_client_status = GameServers.query.filter_by(client_ip=player_ip).first()
    check_connection_status = ClientConnectionList.query \
        .filter_by(client_ip=player_ip, connection_status='playing').first()

    if check_client_status and check_connection_status:
        response['msg'] = 'Please close previous app first'
    else:
        # error handling - has allocated game server to client but game server didn't launched game
        if check_client_status and check_connection_status is None:
            launch_error_handling(check_client_status)

        # choose game server that has the app installed and is also available
        servers = GameServers.query \
            .join(AvailableAppsForServers,
                  AvailableAppsForServers.server_ip == GameServers.server_ip) \
            .filter(AvailableAppsForServers.app_id == app_id) \
            .filter(GameServers.is_available == True).all()
        response['msg'] = 'Not able to allocate edge server at this moment. ' \
                          'Please launch this app later.'
        if servers is not None:  # if there are available edge servers
            for game_server in servers:  # loop through game server list and break once game server is available
                game_server_ip = game_server.server_ip
                logging.info('allocate edge server: ')
                logging.info(game_server_ip)
                req_data = {
                    # "user_id": user_id,
                    "player_ip": player_ip,
                    "app_title": app_title,
                    "app_id": app_id,
                    "platform": platform
                }
                try:
                    server_res = post('http://{0}:8080/game-connection'
                                      .format(game_server_ip), data=req_data, timeout=15)
                    game_server_res = server_res.json()
                    if game_server_res['launch success']:
                        game_server.is_available = False
                        game_server.client_ip = player_ip
                        db.session.commit()

                        response['status'] = True
                        response['msg'] = 'Succesfully allocate edge server... ' \
                                          'connecting then launching the app...'
                        response['game_server_ip'] = game_server_ip
                        break

                except Exception as inst:
                    logging.debug('Edge server error')
                    logging.debug(inst)
                    game_server.is_available = False
                    db.session.commit()
    return response
