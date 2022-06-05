from flask import Blueprint, request, jsonify, json
from application.models.currency import Currency
from helpers.db_helper import Database as db

bp_app = Blueprint('mod_currency', __name__)

#create currency
@bp_app.route('/create_currency', methods=['POST'])
def currency_create():
    data = Currency.currencyCreate()
    return data

#display all currencies
@bp_app.route('/all_currencies', methods=['GET'])
def getCurrencies():
    data = Currency.allCurrencies()
    return data

#delete currency
@bp_app.route('/delete_currency', methods=['DELETE'])
def delete_currency():
    data = Currency.deleteCurrency()
    return data