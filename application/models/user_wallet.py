from abc import abstractstaticmethod
from flask import request, jsonify
from helpers.db_helper import Database as db
from flaskext.mysql import MySQL
import uuid


class UserWallet:
    def __init__(self):
        print('userwallet model')

        #create wallet
    @staticmethod
    def createWallet(userId):
        try:
            
            _wallet_id = uuid.uuid4
            _user_id = userId
            _amount = 0
            _currency_id = "UGX"
            check_user = get_user_details(userId)
            if len(check_user) > 0:
                response = make_response(403, "user already exisisting")
                print(check_user)
                return response

            addWallet_dict = {"wallet_id": _wallet_id, "user_id": _user_id, "amount": _amount, "currency_id": _currency_id }
            data = db.insert('user_wallet', **addWallet_dict)

            return _wallet_id

        except Exception as e:
            print(e)
            response = make_response(403, str(e))
            return response

    
    # delete a wallet
    def deleteWallet():
        try:
            _json = request.json
            _wallet_id = _json['wallet_id']
            sql = "DELETE FROM `user_wallet` WHERE wallet_id = '" + _wallet_id + "' "
            db.delete(sql)
            response = make_response(100, "wallet deleted successfully")
            return response

        except Exception as e:
            print(e)
            response = make_response(403, "failed to delete a wallet")
            return response

    # display all wallets
    @staticmethod
    def allWallets():
        try:
            sql = "SELECT * FROM `user_wallet` "
            data = db.select(sql)
            return jsonify(data)

        except Exception as e:
            print(e)
            response = make_response(403, str(e))
            return response
    
  








#responses
def make_response(status, message):
    return jsonify({"message": message, "status": status})


# get user details basing on e-wallet
def get_user_details(userId):
       sql = "SELECT * FROM `user_wallet` WHERE user_id = '" + str(userId) + "' "
       data = db.select(sql)
       return data