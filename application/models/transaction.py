from abc import abstractstaticmethod
import uuid
from flask import request, jsonify
from helpers.db_helper import Database as db
from flaskext.mysql import MySQL
from application.models.auth import token_required


class Transaction:
    def __init__(self):
        print('transaction model')

        # create user transaction
    @staticmethod
    @token_required
    def createTransaction():
        try:
            _transaction_id = uuid.uuid4()
            _json = request.json
            _from_wallet = _json['from_wallet']
            _to_wallet = _json['to_wallet']
            _transaction_type = _json['transaction_type']
            _amount = _json['amount']
            #_currency_id = _json['currency_id']
            #_wallet_id = _json['wallet_id']
            check_from_user = get_walletDetailsBy_walletId(_from_wallet)
            check_to_user = get_walletDetailsBy_walletId(_to_wallet)
            if len(check_from_user) <= 0:
                response = make_response(403, "Invalid sender account")
                return response
            if len(check_to_user) <= 0:
                response = make_response(403, "invalid receiver account")
                return response
            if check_from_user == check_to_user:
                response = make_response(403, "You can't send money to yourself plz!")
                return response

            if _transaction_type != "P2P":
                response = make_response(403, "Invalid transaction type")
                return response

            check_from_balance = check_from_user[0]['balance']
            if check_from_balance < _amount:
                response = make_response(403, "Not enough funds to make this transaction")
                return response

            if check_from_user[0]['currency_code'] != check_to_user[0]['currency_code']:
                response = make_response(403, "receiver doesn't use same currency as yours!")
                return response

            _from_net_balance = check_from_balance - _amount
            fromupdate_dict = {"balance": _from_net_balance}
            db.Update('user_wallet', "wallet_id = '" + str(_from_wallet) + "'", **fromupdate_dict)

            _to_net_balance = check_to_user[0]['balance'] + _amount
            toupdate_dict = {"balance": _to_net_balance}
            db.Update('user_wallet', "wallet_id = '" + str(_to_wallet) + "'", **toupdate_dict)

            

            _status = "success"


            create_transaction_dict = {"transaction_id": _transaction_id, "from_wallet": _from_wallet, "to_wallet": _to_wallet, "transaction_type": _transaction_type, "amount": _amount}
            data = db.insert('transaction', **create_transaction_dict)
            response = jsonify(100, "transaction statement created")
            return response

        except Exception as e:
            print(e)
            response = jsonify(403, str(e))
            return response

            #display all transactions
    @staticmethod
    @token_required
    def allTransactions():
        sql = "SELECT * FROM `transaction`"
        data = db.select(sql)
        response = jsonify(data)
        return response

        #update transactions
    @staticmethod
    @token_required
    def updateTransaction():
        try:
            _json = request.json
            _from_wallet = _json['from_wallet']
            _to_wallet = _json['to_wallet']
            _transaction_type = _json['transaction_type']
            _amount = _json['amount']
            _currency_id = _json['currency_id']
            _wallet_id = _json['wallet_id']

            update_transaction_dict = {"from_wallet": _from_wallet, "to_wallet": _to_wallet, "transaction_type": _transaction_type, "amount": _amount, "currency_id": _currency_id, "wallet_id": _wallet_id}
            data = db.insert('transaction', **update_transaction_dict)
            response = jsonify(100, "transaction updated ")
            return response

        except Exception as e:
            print(e)
            response = jsonify(403, str(e))
            return response

          #delete transaction
    @staticmethod
    @token_required
    def deleteTransaction():
        try:
            _json = request.json
            _transactionId = _json['transaction_id']
            sql = "DELETE FROM `transaction` WHERE transaction_id = '" + str(_transactionId) + "' "
            db.delete(sql)
            response = jsonify(100, "currency deleted successfully")
            return response
        except Exception as e:
            print(e)
            response = jsonify(403, "failed to delete the currency")
            return response

     # get all transactions basing on the wallet
    @staticmethod
    @token_required
    def allCurrencyWallet():
        try:
            _json = request.json
            _wallet_id = _json['wallet_id']
            check_trans = get_transactions_details(_wallet_id)

            if len(check_trans) <= 0:
                response = make_response(403, "invalid wallet id")
                return response
            
            data = jsonify(check_trans)
            return data

        except Exception as e:
            print(e)
            response = make_response(403, "technical error")
            return response










# responses
def make_response(status, message):
    return jsonify({"message": message, "status": status})

def get_walletDetailsBy_walletId(walletId):
    sql = "SELECT * FROM `user_wallet` WHERE wallet_id = '" + walletId + "' "
    data = db.select(sql)
    return data

#getting all transactions for a specific wallet id
def get_transactions_details(walletId):
    sql = "SELECT * FROM `transaction` WHERE from_wallet = '" + walletId + "' OR to_wallet = '" + walletId + "' "
    data = db.select(sql)
    return data   