import os

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.models import db, Admin
from config import config_options

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'error'

csrf = CSRFProtect()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Bind extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Register structural blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Cross-platform date filter: %-d (Linux) not supported on Windows
    @app.template_filter('datefmt')
    def datefmt_filter(dt, fmt='%-d %B %Y'):
        out = dt.strftime(fmt.replace('%-d', '\x00'))
        return out.replace('\x00', str(dt.day))

    # Create tables on first run (dev convenience)
    with app.app_context():
        db.create_all()

    return app
