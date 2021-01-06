from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# Table of Game servers
class GameServers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_ip = db.Column(db.String(80), unique=True, nullable=False)
    client_ip = db.Column(db.String(80), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    last_connection_at = db.Column(db.DateTime, nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<Gserver id:{0} ip:{1}>'.format(self.id, self.server_ip)


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
    game_id = db.Column(db.Integer, nullable=False)
    game_title = db.Column(db.String(32), nullable=False)
    game_type = db.Column(db.String(32))
    game_brief = db.Column(db.String(256))
    img_url = db.Column(db.String(256))


class WaitingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_ip = db.Column(db.String(32), unique=True, nullable=False)
    server_ip = db.Column(db.String(32), unique=True, nullable=False)

# Way to add new table
# StreamList.__table__.create(db.session.bind)
