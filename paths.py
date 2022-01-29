from app import api, app
from stocks_resource import Stocks
from stock_resource import Stock

api.add_resource(Stocks, "/stocks", methods=["GET"])
api.add_resource(Stock, "/stock", methods=["GET", "POST", "DELETE", "PATCH"])

@app.route("/", methods=["GET"])
def index():
    return "Finance Tracker API"

if __name__ == "__main__":
    # app.run(debug=True) #LocalHost
    app.run(debug=True, host="0.0.0.0") #host on Network
    # app.run(host="0.0.0.0") #host on network no debug