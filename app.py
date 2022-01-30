from datetime import timedelta

from flask import Flask
from flask_restful import Api, fields
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager

app = Flask(__name__)

ACCESS_EXPIRES = timedelta(hours=1)


app.config['JWT_SECRET_KEY'] = 'super-secret' #NEED TO CHANGE THIS TO LOAD FROM FILE, BUT FOR TESTING THIS IS FINE
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_TOKEN_LOCATION'] = ['json', 'headers']
jwt = JWTManager(app)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

stock_resource_fields = {
    'id': fields.Integer,
    'ticker': fields.String,
    'number_of_shares': fields.Float,
    'cost_per_share': fields.Float
}

crypto_resource_fields = {
    'id': fields.Integer,
    'symbol': fields.String,
    'number_of_coins': fields.Float,
    'cost_per_coin': fields.Float
}

if __name__ == '__main__':
    from views import *

    #different ways to start flask server
    app.run(debug=True) #localhost
    # app.run(debug=True, host='0.0.0.0') #host on network
    # app.run(host='0.0.0.0') #host on network no debug