from flask import Flask
from flask_cors import CORS
from .config import Config
from .db import db  
from .routes import api, configure_scheduler
from .controllers import admin_create,create_skills

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)

    app.register_blueprint(api)

    with app.app_context():
        db.create_all()
        admin_create()
        create_skills()

        
    # Configure the session cleanup scheduler
    configure_scheduler(app)
    
    return app


