from flask_pymongo import PyMongo

# Create the PyMongo instance
mongo = PyMongo()

def init_db(app):
    """
    Initialize the database connection and bind it to the app.
    This is necessary for PyMongo to access the database.
    """
    mongo.init_app(app)
