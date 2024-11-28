import bson
import time
from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
import traceback
from .db import mongo


def get_db():
    """
    Configuration method to return db instance
    """
    #db = getattr(g, "db", None)
    #print(getattr(g, "_database", None))

    if 'db' not in g:
        g.db = mongo.db
    return g.db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

def list_accounts():
    try:
        start_time = time.perf_counter()
        
        accounts = list(db.account.find({}).limit(20))
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        query="db.account.find({})"
        return (accounts, execution_time, query)
    except Exception as e:
        traceback.print_exc()
        #return e
        return [], 0, str(e)

def get_account_by_id(account_id):
    try:
        query = "db.account.find({'_id': ObjectId("+account_id+")})"
        start_time = time.perf_counter()
        account = list(db.account.find({"_id": ObjectId(account_id)}))
        #account = list(db.account.find({"accountId": account_id}))
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        return (account, execution_time, str(query))
    except Exception as e:
        return e

def create_account(account_details, include_opp_flag):
    try:
        if 'opportunity' not in account_details:
            start_time = time.perf_counter()
            res = db.account.insert_one(account_details)
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000
            #query = 'db.account.insert_one('+(str(account_details).replace('\n', ' '))+')'
            query='db.account.insert_one(account_details))'
            return(res.acknowledged, execution_time, query)
        else:
            op = account_details['opportunity']
            del account_details['opportunity']
            start_time = time.perf_counter()
            res = db.account.insert_one(account_details)
            opp_res = db.opportunity.insert_one(op)
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000
            query = """START TRANSACTION
            db.acc.insert_one(account_details) 
            db.ops.insert_one(op) 
            END TRANSACTION"""

            return(res.acknowledged, execution_time, query)
    except Exception as e:
        return e

def search_entities(entity_name, search_string):
    try:
        pipeline = [
                        {
                            '$search': {
                            'index': "default",
                            'text': {
                                'query': search_string,
                                'path': {'wildcard': '*'},
                                'fuzzy': {}
                            }
                            }
                        }
                        # {
                        #     '$project': {
                        #     '_id': 0
                        #     }
                        # }
                    ]
        coll = db[entity_name]
        start_time = time.perf_counter()
        entity_res = list(coll.aggregate(pipeline))
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        query = "db."+entity_name+".aggregate("+(str(pipeline).replace('\n', ' '))+")"
        return (entity_res, execution_time, query)
    except Exception as e:
        return e

def list_opportunities():
    try:
        start_time = time.perf_counter()
        opportunities = list(db.opportunity.find({}).limit(20))
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        query="db.opportunity.find({})"
        return (opportunities, execution_time, query)
    except Exception as e:
        return e

def get_opportunity_by_id(opp_id):
    try:
        query = "db.opportunity.find({'_id': ObjectId("+opp_id+")})"
        start_time = time.perf_counter()
        opportunity = list(db.opportunity.find({"_id": ObjectId(opp_id)}))
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        return (opportunity, execution_time, str(query))
    except Exception as e:
        return e

def list_campaigns():
    try:
        start_time = time.perf_counter()
        campaigns = list(db.campaign.find({}).limit(20))
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        query="db.campaign.find({})"
        return (campaigns, execution_time, query)
    except Exception as e:
        return e

def list_interactions():
    try:
        pipeline = [
                    {
                        '$unwind': '$contacts'
                    },
                    {
                        '$unwind': '$contacts.campaignInteractions'
                    },
                    {
                        '$project': {
                        'accountName': '$name',
                        'contactName': '$contacts.name',
                        'campaignId':
                            '$contacts.campaignInteractions.campaignId',
                        'interactionType':
                            '$contacts.campaignInteractions.interactionType'
                        }
                    }
                ]
        start_time = time.perf_counter()
        interactions = list(db.account.aggregate(pipeline))
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        query="db.account.aggregate("+(str(pipeline).replace('\n', ' '))+")"
        return (interactions, execution_time, query)
    except Exception as e:
        return e

def create_campaign(campaign_details):
    try:
        start_time = time.perf_counter()
        res = db.campaign.insert_one(campaign_details)
        end_time = time.perf_counter()
        new_interaction = {"campaignId": campaign_details['campaignId'], "interactionType": "email"}
        q = {'accountId': {'$gte': 2900}}
        u = { "$push": { "contacts.0.campaignInteractions": new_interaction}}
        update_res = db.account.update_many(q, u)
        execution_time = (end_time - start_time) * 1000
        query = 'db.campaign.insert_one('+(str(campaign_details).replace('\n', ' '))+')'
        return(res.acknowledged, execution_time, query)
    except Exception as e:
        return [], 0, str(e)

def campaign_analysis():
    try:
        start_time = time.perf_counter()
        res = (db.campaign_analysis.find_one({}, {'_id': 0}))
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        query = 'db.account.aggregate(analytics_pipeline)'
        return(res, execution_time, query)
    except Exception as e:
        return [], 0, str(e)

def customer_sentiment():
    try:
        start_time = time.perf_counter()
        res = db.tickets.find_one({'customerID': 12345}, {'_id': 0, 'sentiment': 1})
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000
        query = "db.tickets.find_one({'customerID': 12345}, {'_id': 0, 'sentiment': 1})"
        return(res, execution_time, query)

    except Exception as e:
        return [], 0, str(e)


