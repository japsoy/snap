import json
from flask import abort, request, jsonify
from flask_restful import Resource, reqparse
from model.merchant import Merchant
from model.product import Product
from pprint import pprint
import functools
from config import SECRET_KEY
from bson.objectid import ObjectId
import jwt


def login_required(method):
    @functools.wraps(method)
    def wrapper(self):
        header = request.headers.get('Authorization')
        _, token = header.split()
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        except jwt.DecodeError:
            abort(400, message='Token is not valid.')
        except jwt.ExpiredSignatureError:
            abort(400, message='Token is expired.')
        objectid = decoded['user_id']

        merchant = Merchant(id=ObjectId(objectid))
        if not merchant:
            abort(400, message='User is not found.')
        return method(self, merchant)
    return wrapper


class MerchantAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('description', type=str, required=True, help='This field cannot be left blank')

    def get(self):
        test = list(Merchant.objects.all().values())
        for row in test:
            row['_id'] = str(row['_id'])
        return jsonify({
            'status': 'ok',
            'data': test
        })
        return {'message': test}, 404

    def post(self):
        request_data = MerchantAPI.parser.parse_args()
        pprint(request_data)
        if request_data:
            merch = Merchant.objects.create(
                id=ObjectId(),
                name=request_data['name'],
                description=request_data['description'],
            )
            return jsonify({
                'status': 'ok',
                'data': merch.to_dict(with_token=True)
            })
        else:
            return {"response": "param missing"}, 404


class MerchantProductAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('stock', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('price', type=str, required=True, help='This field cannot be left blank')

    @login_required
    def get(self, merchant):
        test = list(Product.objects.raw(
            {'merchant_owner': merchant.pk}
        ).values())

        for row in test:
            row['_id'] = str(row['_id'])
            row['merchant_owner'] = str(row['merchant_owner'])
        return jsonify({
            'status': 'ok',
            'data': test
        })
        return {'message': test}, 404

    @login_required
    def post(self, merchant):
        request_data = MerchantProductAPI.parser.parse_args()
        pprint(request_data)
        if request_data:
            merch = Product.objects.create(
                id=ObjectId(),
                name=request_data['name'],
                stock=request_data['stock'],
                price=request_data['price'],
                merchant_owner=merchant,
            )
            return jsonify({
                'status': 'ok',
                'data': merch.to_dict()
            })
        else:
            return {"response": "param missing"}, 404


class MerchantAPIKey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('_id', type=str, required=True, help='This field cannot be left blank')

    @login_required
    def get(self, merchant):
        return merchant.to_dict()
