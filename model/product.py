from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from .merchant import Merchant


class Product(MongoModel):
    id = fields.ObjectIdField(primary_key=True)
    name = fields.CharField()
    stock = fields.IntegerField()
    price = fields.FloatField()
    merchant_owner = fields.ReferenceField(Merchant)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'snap-app'

    def __str__(self):
        return '%s - %s' % (self.name, self.stock)

    def to_dict(self):
        return {
            '_id': str(self.id),
            'name': self.name,
            'stock': self.stock,
            'stock': self.price,
            'merchant_owner': str(self.merchant_owner.id)
        }
