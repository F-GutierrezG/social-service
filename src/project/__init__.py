import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def register_blueprints(app):
    from project.views.health import health_blueprint
    from project.views.publications import publications_blueprint
    from project.views.categories import categories_blueprint

    app.register_blueprint(health_blueprint)
    app.register_blueprint(publications_blueprint)
    app.register_blueprint(categories_blueprint)


def create_app(script_info=None):
    app = Flask(__name__)

    CORS(app)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
