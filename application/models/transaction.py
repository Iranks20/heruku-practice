from abc import abstractstaticmethod
from flask import request, jsonify
from helpers.db_helper import Database as db
from flaskext.mysql import MySQL


class Transaction:
    def __init__(self):
        print('transaction model')

        # create user transaction
    @staticmethod
    def createTransaction():
        try:
            _json = request.json
            _from_wallet = _json['from_wallet']
            _to_wallet = _json['to_wallet']
            _transaction_type = _json['transaction_type']
            _amount = _json['amount']
            _currency_id = _json['currency_id']
            _wallet_id = _json['wallet_id']

            create_transaction_dict = {"from_wallet": _from_wallet, "to_wallet": _to_wallet, "transaction_type": _transaction_type, "amount": _amount, "currency_id": _currency_id, "wallet_id": _wallet_id}
            data = db.insert('transaction', **create_transaction_dict)
            response = jsonify(100, "transaction statement created")
            return response

        except Exception as e:
            print(e)
            response = jsonify(403, str(e))
            return response

            #display all transactions
    @staticmethod
    def allTransactions():
        sql = "SELECT * FROM `transaction`"
        data = db.select(sql)
        response = jsonify(data)
        return response

        #update transactions
    @staticmethod
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



