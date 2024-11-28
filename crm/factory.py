import os

from flask import Flask, render_template, current_app, g
from flask.json import JSONEncoder
from flask_cors import CORS
from flask_pymongo import PyMongo

from bson import json_util, ObjectId
from datetime import datetime, timedelta

from crm.api.leafy import leafy_api_v1

import os
import configparser

from .db import init_db

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("params.ini")))


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app():

    # Setup paths
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'templates')

    # Initialize Flask app
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
    
    # Enable CORS
    CORS(app, origins="https://leafycrm-frontend-sa-ncr.sa-demo.staging.corp.mongodb.com/")

    # Set custom JSON encoder for the app
    app.json_encoder = MongoJsonEncoder

    # Load MongoDB URI from config
    app.config['MONGO_URI'] = config['PROD']['DB_URI']
    
    # Initialize PyMongo with the Flask app
    init_db(app)

    # @app.before_first_request
    # def before_first_request():
    #     # This is executed before the first request, in the request context
    #     print("App is ready, checking DB connection...")
    #     if mongo.db is None:
    #         print("MongoDB connection failed!")
    #     else:
    #         print("MongoDB connection successful.")

    # APP_DIR = os.path.abspath(os.path.dirname(__file__))
    # #STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    # TEMPLATE_FOLDER = os.path.join(APP_DIR, 'templates')

    # app = Flask(__name__,
    #             template_folder=TEMPLATE_FOLDER,
    #             )
    # CORS(app)
    # app.json_encoder = MongoJsonEncoder
    # app.register_blueprint(leafy_api_v1)
    # app.config['MONGO_URI'] = config['PROD']['DB_URI']
    
    # mongo = PyMongo(app)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('index.html')
    
    # Register blueprint (ensure 'leafy_api_v1' is correctly imported)
    app.register_blueprint(leafy_api_v1)

    return app