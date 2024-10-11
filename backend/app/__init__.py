from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                static_url_path='/static',
                template_folder='templates')
    
    from config import Config
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.inserimento_routes import insert_bp
    app.register_blueprint(insert_bp, url_prefix='/api/')

    from app.routes.lettura_routes import read_bp
    app.register_blueprint(read_bp, url_prefix='/api/')

    from app.routes.quests_ai_routes import quests_ai_bp
    app.register_blueprint(quests_ai_bp, url_prefix='/api/')
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return render_template('index.html')

    # Importa e avvia il thread per il reset delle habits
    with app.app_context():
        from .utils import start_habit_reset_thread
        start_habit_reset_thread()

    return app

# Importa i modelli qui per assicurarti che Flask-Migrate li veda
from app import models
