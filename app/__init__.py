from flask import Flask, make_response
from .db import db, migrate
from .models import task, goal
import os
from .routes.task_routes import bp as tasks_bp
from .routes.goal_routes import bp as goals_bp
from dotenv import load_dotenv

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SLACK_BOT_TOKEN'] = os.environ.get('SLACK_BOT_TOKEN')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    @app.errorhandler(404)
    def handle_404(error):
        return make_response({"message": error.description}, 404)
    
    return app