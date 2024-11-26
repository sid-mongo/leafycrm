from flask import Blueprint, request, jsonify, Flask
from crm.db_crud import list_accounts, get_account_by_id, search_accounts, create_account

from flask_cors import CORS
from crm.api.utils import expect
from datetime import datetime

leafy_api_v1 = Blueprint(
    'leafy_api_v1', 'leafy_api_v1', url_prefix='/api/v1/leafycrm')

@leafy_api_v1.route('/accounts', methods=['GET'])
def api_list_accounts():
    #ACCOUNTS_PER_PAGE = 20
    accounts = list_accounts()
    
    response = {
        "accounts": accounts,
        "page": 0,
        "filters": {}
    }
    return jsonify(response)

@leafy_api_v1.route('/accounts/<account_id>', methods=['GET'])
def api_get_account_by_id(account_id):
    (account, query) = get_account_by_id(account_id)
    
    response = {
        "accounts": account,
        "page": 0,
        "query": query
    }
    return jsonify(response)

@leafy_api_v1.route('/accounts/search', methods=['GET'])
def api_search_accounts():
    name = request.args.get('name')
    (account, query) = search_accounts(name)
    
    response = {
        "accounts": account,
        "page": 0,
        "query": query
    }
    return jsonify(response)

@leafy_api_v1.route('/accounts', methods=['POST'])
def api_create_account():
    (account) = create_account(request.get_json())
    response = {
        "accounts": account,
        "page": 0,
        "query": ""
    }
    return jsonify(response)