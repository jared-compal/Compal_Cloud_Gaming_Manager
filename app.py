from flask import Flask, request, jsonify
from Models import db, GameServers, StreamList, datetime, WaitingList
from requests import get, post
from list_service import list_service
from web_portal.web_portal import portal
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# MySql database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Aa123456@127.0.0.1:3306/cloud_game_db"
db.init_app(app)

app.register_blueprint(list_service)
app.register_blueprint(portal, url_prefix='/portal')
# cloudXR_client_cmd = "C:\Program Files\Nvidia Corporation\CloudXR\Client\CLoudXRClient.exe -w"


@app.route('/')
def index():
    db.create_all()
    return "DB sync"


# Register game server
@app.route('/registration')
def register_game_server():
    g_server_ip = request.remote_addr
    print('register', g_server_ip)
    get_register(g_server_ip)
    return g_server_ip + ' game server registered'


# Disconnection signal from game server
@app.route('/cancellation')
def unregister_game_server():
    g_server_ip = request.remote_addr
    print('disconnect', g_server_ip)
    query = GameServers.query.filter_by(server_ip=g_server_ip).first()

    if query:
        query.is_available = False
        StreamList.query.filter_by(server_ip=g_server_ip).delete()
        db.session.commit()

    return g_server_ip + ' disconnected'


@app.route('/games/<string:game_id>/launch', methods=['GET'])
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


@app.route('/streaming', methods=['POST'])
def streaming():
    stream_info = {
        'stream_ip': request.form.get('stream_ip', type=str),
        'game_title': request.form.get('game_title', type=str),
        'player_ip': request.form.get('player_ip', type=str)
    }
    if register_stream(dict):
        return {'status': True,
                'msg': 'Successfully create streaming channel'}
    return {
            'status': False,
            'msg': "Couldn't create streaming channel"
            }


@app.route('/clean')
def clean_streams():
    StreamList.query.delete()
    WaitingList.query.delete()
    db.session.commit()
    return 'table cleaned'


def save_stream_source(game_server_ip, gamer_ip, game_id):
    new_stream = StreamList(server_ip=game_server_ip, client_ip=gamer_ip, game_title=game_id)
    db.session.add(new_stream)
    db.session.commit()
    print('Stream created')


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
    #TBD
    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
