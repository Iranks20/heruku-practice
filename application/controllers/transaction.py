from urllib import response
from flask import Blueprint, request, jsonify, json
from application.models.transaction import Transaction

bp_app = Blueprint('mod_transaction', __name__)

# create transactions
@bp_app.route('/user_create_transaction', methods=['POST'])
def create_transaction():
    data = Transaction.createTransaction()
    return data

    #dsplay transactions
@bp_app.route('/all_transactions', methods=['GET'])
def getTransactions():
        data = Transaction.allTransactions()
        return data

        #update transations
@bp_app.route('/update_transaction', methods=['POST'])
def update_transaction():
    data = Transaction.updateTransaction()
    return data

    #delete transaction
@bp_app.route('/delete_transaction', methods=['DELETE'])
def delete_transaction():
        data = Transaction.deleteTransaction()
        return data