import os
import socket


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Aa123456@127.0.0.1:3306/cloud_game_db"
    SECRET_KEY = os.urandom(32)
    # IP = socket.gethostbyname(socket.gethostname())
    IP = '127.0.0.1'

    # Flask-User settings
    USER_ENABLE_EMAIL = False  # Enable email authentication
    USER_ENABLE_USERNAME = False  # Disable username authentication
