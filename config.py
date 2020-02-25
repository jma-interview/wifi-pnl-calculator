SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

class Config:
    SECRET_KEY = SECRET_KEY
    CONN = 'default'
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'

    DEBUG = True
    TESTING = True
    DEVELOPMENT = True

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEVELOPMENT = False
    TESTING = False
    DEBUG = False


config = {
    'dev': Config,
    'prod': ProductionConfig,

    'default': Config
}
