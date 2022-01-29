from flask import Flask
from flask_restful import Api, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

resource_fields = {
    'id': fields.Integer,
    'ticker': fields.String,
    'current_price': fields.Float,
    'number_of_shares': fields.Float,
    'market_value': fields.Float
}

if __name__ == '__main__':
    from views import *

    #different ways to start flask server
    #app.run(debug=True) #LocalHost
    app.run(debug=True, host='0.0.0.0') #host on Network
    #app.run(host='0.0.0.0') #host on network no debug