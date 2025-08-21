import os
from flask import Flask
from config import Config
from .models import db
from flask_migrate import Migrate # 匯入 Migrate

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db) # 初始化 Migrate

    # Register blueprints
    from .api.habits import habits_bp
    from .api.auth import auth_bp
    from .api.moods import moods_bp
    from .api.trackings import trackings_bp

    app.register_blueprint(habits_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(moods_bp, url_prefix='/api')
    app.register_blueprint(trackings_bp, url_prefix='/api')

    return app