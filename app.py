from flask import Flask
from api.merchant_api import MerchantProductAPI, MerchantAPIKey, MerchantAPI
from flask_restful import Api
import mongo_config

app = Flask(__name__)
api = Api(app)

api.add_resource(MerchantAPI, '/merchant/')
api.add_resource(MerchantAPIKey, '/merchant-api/')

api.add_resource(MerchantProductAPI, '/merchant-product/')

if __name__  == "__main__":
    app.run(debug=True)
