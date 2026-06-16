import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qhamuka_secret_key_1880s'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Fallback to SQLite for development, ready for MySQL in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'qhamuka.db')

    # File uploads (gallery images)
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB cap per upload
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Example MySQL URI:
    # 'mysql+pymysql://user:password@host/dbname'


config_options = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
