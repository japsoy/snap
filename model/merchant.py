from pymongo.write_concern import WriteConcern
import datetime
from pymodm import MongoModel, fields
import functools
import jwt
from config import SECRET_KEY


class Merchant(MongoModel):
    id = fields.ObjectIdField(primary_key=True)
    name = fields.CharField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'snap-app'

    def __str__(self):
        return '%s %s' % (self.name, self.description)

    def encode_auth_token(self):
        user_id = str(self.id)
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
                'iat': datetime.datetime.utcnow(),
                'user_id': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def to_dict(self, with_token=False):
        merchant = {
            '_id': str(self.id),
            'name': self.name,
            'description': self.name,
        }

        if with_token:
            merchant['token'] = self.encode_auth_token()
        return merchant
