from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# from flask_wtf.csrf import CSRFProtect
from manager.config import Config

# MySql database
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_service.user_login'
    login_manager.blueprint_login_views = {
        'portal': 'portal.login_page',
        'backstage': 'portal.login_page'
    }
    login_manager.login_message = 'Please login to access this website'
    login_manager.login_message_category = 'info'
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    from manager.main.routes import main
    from manager.list_service.list_service import list_service
    from manager.web_portal.web_portal import portal
    from manager.auth.auth_service import auth_service
    from manager.backstage.backstage import backstage
    app.register_blueprint(main)
    app.register_blueprint(list_service)
    app.register_blueprint(portal, url_prefix='/portal')
    app.register_blueprint(auth_service)
    app.register_blueprint(backstage, url_prefix='/backstage')

    return app
