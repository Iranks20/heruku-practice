from urllib import response
from flask import request, jsonify
from helpers.db_helper import Database as db
import uuid
from application.models.auth import token_required



class UserWallet:
    def __init__(self):
        print('userwallet model')
        #create wallet
    @staticmethod
    def createWallet(userId):
        try:
            
            _wallet_id = uuid.uuid4()
            _user_id = userId
            _balance = 0
            _currency_code = "UGX"

            addWallet_dict = {"wallet_id": _wallet_id, "user_id": _user_id, "balance": _balance, "currency_code": _currency_code }
            data = db.insert('user_wallet', **addWallet_dict)

            return _wallet_id

        except Exception as e:
            print(e)
            response = make_response(403, str(e))
            return response


    # creating other wallets
    def otherWallets():
        try:
            _json = request.json
            _user_id = _json['user_id']
            _currency_code = _json['currency_code']
            balance = 0.0
            _wallet_id = uuid.uuid4()

            # check if user exists
            check_user = get_user_details(_user_id)
            if len(check_user) <= 0:
                response = make_response(403, "invalid user")
                return response

            # check user wallet if it already exists
            check_wallet = get_user_details(_user_id)
            check_wallet_currency_code = check_wallet[0]['currency_code']
            if _currency_code == check_wallet_currency_code:
                response = make_response(403, "wallet type already exits")
                return response

            other_wallet_dict = {"user_id": _user_id, "wallet_id": _wallet_id, "balance": balance, "currency_code": _currency_code}

            db.insert('user_wallet', **other_wallet_dict)

            response = make_response(100, "New Wallet created successfully")
            return response
        except Exception as e:
            print(e)
            response = make_response(403, "failed to create a new wallet")
            return response
        

    
    # delete a wallet
    def deleteWallet():
        try:
            _json = request.json
            _wallet_id = _json['wallet_id']

            check_wallet = get_wallet_details(_wallet_id)
            check_wallet_balance = check_wallet[0]['balance']
            if check_wallet_balance != 0.0:
                response = make_response(403, "wallet with money cant be deleted")
                return response


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
    @token_required 
    def allWallets():
        try:
            sql = "SELECT * FROM `user_wallet` "
            data = db.select(sql)
            return jsonify(data)

        except Exception as e:
            print(e)
            response = make_response(403, str(e))
            return response

    # wallet details basing on user id
    @token_required
    def getWalletDetails():
        try:
            _json = request.json
            _user_id = _json['user_id']

            data = get_user_details(_user_id)
            response = jsonify(data)
            if len(data) <= 0:
                print(data)
                return make_response(403, "No wallet for User ID " + str(_user_id) + "!")
            return response

        except Exception as e:
            print(e)
            response = make_response(403, "syntax error")
            return response
    
  








#responses
def make_response(status, message):
    return jsonify({"message": message, "status": status})


# get user details basing on e-wallet
def get_user_details(userId):
    sql = "SELECT * FROM `user_wallet` WHERE user_id = '" + str(userId) + "' "
    data = db.select(sql)
    return data

#get wallet details
def get_wallet_details(wallet_id):
    sql = "SELECT * FROM user_wallet WHERE wallet_id = '" + wallet_id + "' "
    data = db.select(sql)
    return data
        