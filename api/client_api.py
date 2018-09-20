import json
from flask import abort, request, jsonify
from flask_restful import Resource, reqparse
from model.merchant import Product
from model.product import Client
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

        client = Client(id=ObjectId(objectid))
        if not client:
            abort(400, message='User is not found.')
        return method(self, client)
    return wrapper


class ClientAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('email', type=str, required=True, help='This field cannot be left blank')

    def get(self):
        test = list(Client.objects.all().values())
        for row in test:
            row['_id'] = str(row['_id'])
        return jsonify({
            'status': 'ok',
            'data': test
        })
        return {'message': test}, 404

    def post(self):
        request_data = ClientAPI.parser.parse_args()
        if request_data:
            merch = Client.objects.create(
                _id=ObjectId(),
                name=request_data['name'],
                email=request_data['email'],
            )
            return jsonify({
                'status': 'ok',
                'data': merch.to_dict(with_token=True)
            })
        else:
            return {"response": "param missing"}, 404

