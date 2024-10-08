from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                static_url_path='/static',
                template_folder='templates')
    
    from config import Config
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)

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

    return app
