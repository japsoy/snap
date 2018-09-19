from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields


class User(MongoModel):
    email = fields.EmailField(primary_key=True)
    first_name = fields.CharField()
    last_name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'snap-app'

    def __str__(self):
        return '%s %s %s' % (self.email, self.first_name, self.last_name)