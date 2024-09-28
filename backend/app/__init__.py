from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    from config import Config
    app.config.from_object(Config)

    # Inizializza CORS prima di registrare i blueprint
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


    db.init_app(app)

    from app.routes.inserimento_routes import insert_bp
    app.register_blueprint(insert_bp, url_prefix='/api/')

    from app.routes.lettura_routes import read_bp
    app.register_blueprint(read_bp, url_prefix='/api/')

    from .routes.quests_ai_routes import quests_ai_bp
    app.register_blueprint(quests_ai_bp, url_prefix='/api/')

    return app
