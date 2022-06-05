from operator import methodcaller
from unittest import expectedFailure
import pymysql
from flask import jsonify, request
from helpers.db_helper import Database as db
from abc import abstractstaticmethod
from flaskext.mysql import MySQL

class Currency:
    def __init__(self):
        print('currency model')
#create currency
    @staticmethod
    def currencyCreate():
        try: 
            _json = request.json
            _currency_name = _json['currency_name']
            _currency_code = _json['currency_code']
        
       #check_currency = get_currency_details(_currency_name, _currency_code)
        #if len (check_currency) > 0:
            ##return response

            createCurrency_dict = {"currency_name": _currency_name, "currency_code": _currency_code }
            data = db.insert('currencies', **createCurrency_dict)
            response = jsonify(100, "currecny created successfully")
            return response
    
        except Exception as e:
            print(e)
            response = jsonify({"message": str(e)})
            return response

#display all currencies
    @staticmethod
    def allCurrencies():
        sql = "SELECT * FROM `currencies`"
        data = db.select(sql)
        response = jsonify(data)
        return response

#delete currency
    @staticmethod
    def deleteCurrency():
        try:
            _json = request.json
            _currencyId = _json['currency_id']
            sql = "DELETE FROM `currencies` WHERE currency_id = '" + str(_currencyId) + "' "
            db.delete(sql)
            response = jsonify(100, "currency deleted successfully")
            return response
        except Exception as e:
            print(e)
            response = jsonify(403, "failed to delete the currency")
            return response







#def make_response(status, message):
    #return jsonify({"message":message, "status":status})

def get_currency_details(Currency_name, currency_code):
    sql = "SELECT * FROM `currencies` WHERE currency_code ='" + currency_code + "' OR currency_name = '" + Currency_name + "' "
    data = db.select(sql)
    return data