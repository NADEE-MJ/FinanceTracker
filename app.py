from flask import Flask
from flask_restful import Api, reqparse, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

resourceFields = {
    'id': fields.Integer,
    'ticker': fields.String,
    'currentPrice': fields.Float,
    'numberOfShares': fields.Float,
    'marketValue': fields.Float
}

if __name__ == "__main__":

    from views import *

    # app.run(debug=True) #LocalHost
    app.run(debug=True, host="0.0.0.0") #host on Network
    # app.run(host="0.0.0.0") #host on network no debug