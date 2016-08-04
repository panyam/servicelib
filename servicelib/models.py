
from google.appengine.ext import ndb

class ModelBase(ndb.Model):
    def getid(self):
        return str(self.key.id())

