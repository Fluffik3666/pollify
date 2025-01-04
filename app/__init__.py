# app/__init__.py
from flask import Flask, send_from_directory
import os
import json
from config import Config
from firebase_admin import initialize_app, credentials

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    
    # Initialize Firebase with JSON credentials from environment variable
    cred_dict = json.loads(os.environ.get('FIREBASE_CREDENTIALS'))
    cred = credentials.Certificate(cred_dict)
    initialize_app(cred, {
        'databaseURL': os.environ.get('FIREBASE_DB_URL')
    })
    
    # Serve static files
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(app.static_folder, filename)

    # Serve favicon
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app