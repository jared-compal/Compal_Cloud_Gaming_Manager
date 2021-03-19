from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
# from flask_wtf.csrf import CSRFProtect
from manager.config import Config, Local

# MySql database
db = SQLAlchemy()
bcrypt = Bcrypt()
# login_manager = LoginManager()
jwt = JWTManager()


def create_app():
    config_class = Config
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    from manager.main.routes import main
    from manager.list_service.list_service import list_service
    from manager.web_portal.web_portal import portal
    from manager.auth.auth_service import auth_service
    # from manager.models import User
    from manager.streaming.streaming_service import streaming_service
    app.register_blueprint(main)
    app.register_blueprint(list_service)
    app.register_blueprint(portal, url_prefix='/portal')
    app.register_blueprint(auth_service)
    app.register_blueprint(streaming_service, url_prefix='/streaming')
    return app

