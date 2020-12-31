from flask import Blueprint, jsonify

list_service = Blueprint('list_service', __name__)
# SERVER_ADDR = 'http://172.16.0.25:5000'
SERVER_ADDR = 'http://localhost:5000'


@list_service.route('/streams')
def show_streams():
    data = {
            "status": True,
            "total_num": 2,
            "streams": {
                0: {
                    "stream_id": 0,
                    "stream_title": "Gunjack",
                    "stream_brief": "Jump into your weapons turret and annihilate endless waves of enemies.",
                    "img_url": "",
                    "stream_url": "",
                    "player_info": "Johnson"
                },
                1: {
                    "stream_id": 1,
                    "stream_title": "Redout",
                    "stream_brief": "An uncompromising, fast, tough and satisfying car racing game!",
                    "img_url": "",
                    "stream_url": "",
                    "player_info": "PewDiePie"
                }
            }}
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@list_service.route('/streams/<string:stream_id>')
def show_stream(stream_id):
    return "get {0} info".format(stream_id)


@list_service.route('/games')
def show_games():
    data = {
            "status": True,
            "total_num": 2,
            "games": {
                0: {
                    "game_id": 0,
                    "game_title": "Gunjack",
                    "game_type": "FPS",
                    "game_brief": "Jump into your weapons turret and annihilate endless waves of enemies.",
                    "img_url": "{0}/static/games_icon/gunjack.jpg".format(SERVER_ADDR)
                },
                1: {
                    "game_id": 1,
                    "game_title": "Redout",
                    "game_type": "Car Racing",
                    "game_brief": "An uncompromising, fast, tough and satisfying car racing game!",
                    "img_url": "{0}/static/games_icon/redout.jpg".format(SERVER_ADDR)
                }
            }}
    resp = jsonify(data)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@list_service.route('/games/<string:game_id>')
def show_game(game_id):
    return "get {0} info".format(game_id)
