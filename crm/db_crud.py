import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db
    return db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

def list_accounts():
    try:
        accounts = list(db.Accounts.find({}, {"_id": 0}))
        return accounts
    except Exception as e:
        return e

def get_account_by_id(account_id):
    try:
        query = "db.Accounts.find({'AccountID':"+account_id+"}, {'_id': 0})"
        account = list(db.Accounts.find({"AccountID": account_id}, {"_id": 0}))
        return (account, str(query))
    except Exception as e:
        return e

def search_accounts(name):
    try:
        
        pipeline = [
                    {
                        '$match': {
                            'AccountName': name
                        }
                    }, {
                        '$project': {
                            '_id': 0
                        }
                    }
                ]
        account = list(db.Accounts.aggregate(pipeline))
        query = "db.Accounts.aggregate("+(str(pipeline).replace('\n', ''))+")"
        return (account, query)
    except Exception as e:
        return e

def create_account(account_details):
    try:
        #print(account_details['hello'])
        return("hello")
    except Exception as e:
        return e
