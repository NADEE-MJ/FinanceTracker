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

#run this file once to create the db file in the main directory
if __name__ == "__main__":
    db.create_all()