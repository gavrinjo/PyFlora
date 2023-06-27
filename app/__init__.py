from flask import Flask, abort
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


class ModleViewController(ModelView):
    def is_accessible(self):
        if current_user.is_admin:
            return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class AdminViewController(AdminIndexView):
    def is_accessible(self):
        if current_user.is_admin:
            return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
admin = Admin(name='PyFlora', index_view=AdminViewController())


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        db.create_all()
        return app


from app import models

admin.add_view(ModleViewController(models.User, db.session))
admin.add_view(ModleViewController(models.Pot, db.session))
admin.add_view(ModleViewController(models.Plant, db.session))