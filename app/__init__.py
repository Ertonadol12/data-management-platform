from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    from app.routes import auth, main, upload, clean, report, history, profile, preview
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(clean.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(history.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(preview.bp)
    
    from app.models import user, upload, processed, metrics
    
    @app.context_processor
    def utility_processor():
        return {'now': __import__('datetime').datetime.now}
    
    return app