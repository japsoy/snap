from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields


class Merchant(MongoModel):
    name = fields.CharField()
    description = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'snap-app'

    def __str__(self):
        return '%s %s' % (self.name, self.description)
