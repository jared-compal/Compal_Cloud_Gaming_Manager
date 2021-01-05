from flask import Blueprint, jsonify


SERVER_ADDR = 'http://172.16.0.25:5000'
# SERVER_ADDR = 'http://localhost:5000'
list_service = Blueprint('list_service', __name__)


@list_service.route('/streams')
def show_streams():
    data = {
            "status": True,
            "total_num": 2,
            "streams": {
                0: {
                    "content_id": 0,
                    "content_title": "League of legend",
                    "content_brief": "Jump into your weapons turret and annihilate endless waves of enemies.",
                    "img_url": "{0}/static/streams_icon/live_user_chiao622.jpg".format(SERVER_ADDR),
                    "content_url": "",
                    "player_info": "Chiao622"
                },
                1: {
                    "content_id": 1,
                    "content_title": "Redout",
                    "content_brief": "An uncompromising, fast, tough and satisfying car racing game!",
                    "img_url": "{0}/static/streams_icon/live_user_lol_ambition.jpg".format(SERVER_ADDR),
                    "content_url": "",
                    "player_info": "Ambition"
                }
            }}
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@list_service.route('/streams/<string:stream_id>')
def show_stream(stream_id):
    data = {
            "status": True,
            "stream": {
                "content_id": 0,
                "content_title": "League of legend",
                "content_brief": "Jump into your weapons turret and annihilate endless waves of enemies.",
                "img_url": "{0}/static/streams_icon/live_user_chiao622.jpg".format(SERVER_ADDR),
                "content_url": "",
                "player_info": "Chiao622"
                }
            }
    return data


@list_service.route('/games')
def show_games():
    data = {
            "status": True,
            "total_num": 2,
            "games": {
                0: {
                    "content_id": 0,
                    "content_title": "Gunjack",
                    "content_type": "FPS",
                    "content_brief": "Jump into your weapons turret and annihilate endless waves of enemies.",
                    "img_url": "{0}/static/games_icon/gunjack.jpg".format(SERVER_ADDR)
                },
                1: {
                    "content_id": 1,
                    "content_title": "Redout",
                    "content_type": "Car Racing",
                    "content_brief": "An uncompromising, fast, tough and satisfying car racing game!",
                    "img_url": "{0}/static/games_icon/redout.jpg".format(SERVER_ADDR)
                }
            }}
    resp = jsonify(data)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@list_service.route('/games/<string:game_id>')
def show_game(game_id):
    data = {
            "status": True,
            "game": {
                "content_id": 0,
                "content_title": "Gunjack",
                "content_type": "FPS",
                "content_brief": "Jump into your weapons turret and annihilate endless waves of enemies.",
                "img_url": "{0}/static/games_icon/gunjack.jpg".format(SERVER_ADDR)
            }
    }
    return data
