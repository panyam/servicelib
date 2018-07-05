
class BaseModel(object):
    """ Base interface of all DAO models. """
    @classmethod
    def delete_all(cls):
        """ Deletes all instances of this model from the underlying store. """
        raise Exception("Not Implemented")

    @classmethod
    def getraw(cls, obj_or_id, nothrow = False, cachekey = None):
        """ A raw loader method for an object of this model given its ID. """
        raise Exception("Not Implemented")

    def getid(self):
        """ Get's the object's ID. """
        raise Exception("Not Implemented")

    def delete(self):
        """ Kick's off a deletion of this object. """
        raise Exception("Not Implemented")

