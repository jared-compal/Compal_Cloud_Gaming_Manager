from manager import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Table of Game servers
class GameServers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_ip = db.Column(db.String(80), unique=True, nullable=False)
    client_ip = db.Column(db.String(80), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    last_connection_at = db.Column(db.DateTime, nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    db_available_games = db.relationship("AvailableGamesForServers", backref="server")

    def __repr__(self):
        return '<Gserver id:{0} ip:{1}>'.format(self.id, self.server_ip)


class AvailableGamesForServers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(32), nullable=False)
    server_ip = db.Column(db.String(80), db.ForeignKey('game_servers.server_ip'), nullable=False)


class StreamList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_ip = db.Column(db.String(32), unique=True, nullable=False)
    client_ip = db.Column(db.String(32), unique=True, nullable=False)
    client_username = db.Column(db.String(62), nullable=True)
    stream_title = db.Column(db.String(64), nullable=False)
    num_of_audience = db.Column(db.Integer, default=0)
    img_url = db.Column(db.String(128))
    stream_url = db.Column(db.String(128))
    started_from = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class GameList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(32), nullable=False)
    game_title = db.Column(db.String(32), nullable=False)
    game_type = db.Column(db.String(32))
    game_brief = db.Column(db.String(256))
    img_url = db.Column(db.String(256))


class ClientConnectionList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), unique=False, nullable=True)
    client_ip = db.Column(db.String(32), unique=False, nullable=False)
    server_ip = db.Column(db.String(32), unique=False, nullable=False)
    game_id = db.Column(db.String(32), unique=False, nullable=False)
    connection_status = db.Column(db.String(32), nullable=False)
    launch_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    close_time = db.Column(db.DateTime, nullable=True)
    total_play_time = db.Column(db.BigInteger, nullable=True,
                                default=0)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
