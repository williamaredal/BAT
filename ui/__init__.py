############ Initializes App ############
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Gets App Configuration
    app.config.from_object('config.Config')

    # Initializes db and login manager plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from .import dossier
        from .assets import compile_static_assets

        # Registrates blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(dossier.dossier_bp)

        # Creates the database models
        db.create_all()

        # Compiles static assets
        if app.config['FLASK_ENV'] == 'development':
            compile_static_assets(app)

        return app