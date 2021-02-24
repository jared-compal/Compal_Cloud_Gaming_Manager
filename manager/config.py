import os
import socket
from datetime import timedelta


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Aa123456@127.0.0.1:3306/cloud_game_db"
    SECRET_KEY = os.urandom(32)
    IP_TUPLE = socket.gethostbyname_ex(socket.gethostname())
    IP = IP_TUPLE[2][0]     # In case machine has multiple IP addresses
    SERVER_ADDR = 'http://{0}:5000'.format(IP)
    # JWT_SECRET_KEY = os.urandom(16)
    JWT_SECRET_KEY = "os.urandom(16)"
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=60)
    # https://cdn.cloudflare.steamstatic.com/steam/apps/410570/header.jpg?t=1570790651
    # https://cdn.cloudflare.steamstatic.com/steam/apps/517710/header.jpg?t=1589270416


class Local(Config):
    IP = '127.0.0.1'
