from flask import Blueprint, request, jsonify, Flask, current_app, g, Response
from crm.db_crud import list_accounts, get_account_by_id, create_account, customer_sentiment, search_entities, list_opportunities, get_opportunity_by_id, list_campaigns, list_interactions, create_campaign, campaign_analysis

from flask_cors import CORS, cross_origin
from crm.api.utils import expect
from datetime import datetime
import json

leafy_api_v1 = Blueprint(
    'leafy_api_v1', 'leafy_api_v1', url_prefix='/api/v1/leafycrm')

CORS(leafy_api_v1, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@leafy_api_v1.route('/accounts', methods=['GET'])
@cross_origin(origins="https://leafycrm-frontend-sa-ncr.sa-demo.staging.corp.mongodb.com/", supports_credentials=True, methods=['GET', 'POST'])
def api_list_accounts():
    
    (accounts, execution_time, query) = list_accounts()
    resp = {
        "accounts": accounts,
        "execution_time": execution_time,
        "query": query,
    }
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return response

@leafy_api_v1.route('/accounts/<account_id>', methods=['GET'])
def api_get_account_by_id(account_id):
    (account, execution_time, query) = get_account_by_id(account_id)
    
    response = {
        "accounts": account,
        "execution_time": execution_time,
        "query": query
    }
    return jsonify(response)

@leafy_api_v1.route('/accounts', methods=['POST'])
def api_create_account():
    include_opp_flag = request.args.get('includesOpp')
    (res, execution_time, q) = create_account(request.get_json(), include_opp_flag)
    response = {
        "accounts": res,
        "execution_time": execution_time,
        "query": q
    }
    return jsonify(response)

@leafy_api_v1.route('/search', methods=['GET'])
def api_search_entities():
    search_term = request.args.get('search_term')
    search_entity = request.args.get('search_entity')
    (entity_res, execution_time, query) = search_entities(search_entity, search_term)
    
    response = {
        search_entity: entity_res,
        "execution_time": execution_time,
        "query": query
    }
    return jsonify(response)

@leafy_api_v1.route('/opportunities', methods=['GET'])
def api_list_opportunities():
    
    (opportunities, execution_time, query) = list_opportunities()
    response = {
        "opportunities": opportunities,
        "execution_time": execution_time,
        "query": query,
    }
    return jsonify(response)

@leafy_api_v1.route('/opportunities/<opp_id>', methods=['GET'])
def api_get_opportunity_by_id(opp_id):
    (opportunity, execution_time, query) = get_opportunity_by_id(opp_id)
    
    response = {
        "opportunities": opportunity,
        "execution_time": execution_time,
        "query": query
    }
    return jsonify(response)

@leafy_api_v1.route('/campaigns', methods=['GET'])
def api_list_campaigns():
    
    (campaigns, execution_time, query) = list_campaigns()
    response = {
        "campaigns": campaigns,
        "execution_time": execution_time,
        "query": query,
    }
    return jsonify(response)

@leafy_api_v1.route('/interactions', methods=['GET'])
def api_list_interactions():
    
    (interactions, execution_time, query) = list_interactions()
    response = {
        "interactions": interactions,
        "execution_time": execution_time,
        "query": query,
    }
    return jsonify(response)

@leafy_api_v1.route('/campaigns', methods=['POST'])
def api_create_campaign():
    
    (res, execution_time, q) = create_campaign(request.get_json())
    response = {
        "campaign": res,
        "execution_time": execution_time,
        "query": q
    }
    return jsonify(response)

@leafy_api_v1.route('/campaign_analysis', methods=['GET'])
def api_campaign_analysis():
    
    (res, execution_time, q) = campaign_analysis()
    response = {
        "campaign": res,
        "execution_time": execution_time,
        "query": q
    }
    return jsonify(res)

@leafy_api_v1.route('/customer_sentiment', methods=['GET'])
def api_customer_sentiment():
    
    (res, execution_time, q) = customer_sentiment()
    response = {
        "campaign": res,
        "execution_time": execution_time,
        "query": q
    }
    return jsonify(response)