import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, abort
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_bootstrap import Bootstrap5
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_moment import Moment
import os


class ModleViewController(ModelView):
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash']
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class AdminViewController(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
mail = Mail()
bootstrap = Bootstrap5()
admin = Admin(name='PyFlora', index_view=AdminViewController(), template_mode='bootstrap4')
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    images = UploadSet('images', IMAGES)
    configure_uploads(app, images)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)
    moment.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.pyflora import bp as pyflora_bp
    app.register_blueprint(pyflora_bp)

    with app.app_context():
        db.create_all()
    
    import app.errors.error_logger as log
    log.get_logger(app, 'logfile')

    # if not app.debug:
    #     if app.config['MAIL_SERVER']:
    #         auth = None
    #         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    #         secure = None
    #         if app.config['MAIL_USE_TLS']:
    #             secure = ()
    #         mail_handler = SMTPHandler(
    #             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #             toaddrs=app.config['ADMINS'], subject='pyFlora Failure',
    #             credentials=auth, secure=secure)
    #         mail_handler.setLevel(logging.ERROR)
    #         app.logger.addHandler(mail_handler)

    #     if app.config['LOG_TO_STDOUT']:
    #         stream_handler = logging.StreamHandler()
    #         stream_handler.setLevel(logging.INFO)
    #         app.logger.addHandler(stream_handler)
    #     else:
    #         if not os.path.exists('logs'):
    #             os.mkdir('logs')
    #         file_handler = RotatingFileHandler('logs/logfile.log', maxBytes=10240, backupCount=10)
    #         file_handler.setFormatter(logging.Formatter(
    #             '%(asctime)s %(levelname)s: %(message)s '
    #             '[in %(pathname)s:%(lineno)d]'))
    #         file_handler.setLevel(logging.INFO)
    #         app.logger.addHandler(file_handler)
    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('pyFlora startup')
    return app


from app import models

admin.add_view(ModleViewController(models.User, db.session))
admin.add_view(ModleViewController(models.Pot, db.session))
admin.add_view(ModleViewController(models.Sensor, db.session))
admin.add_view(ModleViewController(models.Reading, db.session))
admin.add_view(ModleViewController(models.Plant, db.session))
admin.add_view(ModleViewController(models.Value, db.session))
admin.add_view(ModleViewController(models.Gauge, db.session))

path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, name='Static Files'))