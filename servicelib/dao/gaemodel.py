
import datetime
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users
import errors, models

class GAEBaseModel(models.BaseModel, ndb.Model):
    @classmethod
    def delete_all(cls):
        keys = cls.query().fetch(1000, keys_only = True)
        while keys:
            ndb.delete_multi(keys)
            keys = cls.query().fetch(1000, keys_only = True)

    @classmethod
    def getraw(cls, obj_or_id, nothrow = False, cachekey = None):
        obj = obj_or_id
        if not issubclass(obj.__class__, ModelBase):
            if issubclass(obj_or_id.__class__, ndb.Key):
                obj = cls.get_by_id(obj_or_id.id())
            else:
                obj = None
                if cachekey is not None:
                    obj = memcache.get(cachekey)
                if obj is None:
                    obj = cls.get_by_id(obj_or_id)
            if obj is None:
                if nothrow: return None
                else: raise errors.NotFound("Object not found for ID: " + str(obj_or_id))
        return obj

    def getid(self):
        return self.key.id()

    def delete(self):
        ndb.delete_multi([self.key])
