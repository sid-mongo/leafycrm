from crm.factory import create_app
from flask_pymongo import PyMongo
import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("params.ini")))

if __name__ == "__main__":
    
    app = create_app()
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = config['PROD']['DB_URI']
    
    app.run(debug=True, port=5001)