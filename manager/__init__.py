from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from manager.config import Config

# MySql database
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    from manager.main.routes import main
    from manager.list_service.list_service import list_service
    from manager.web_portal.web_portal import portal
    from manager.auth.auth_service import auth_service
    app.register_blueprint(main)
    app.register_blueprint(list_service)
    app.register_blueprint(portal, url_prefix='/portal')
    app.register_blueprint(auth_service)

    return app
