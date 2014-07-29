from arangodb.api import Collection


class CollectionModel(object):

    collection_instance = None

    @classmethod
    def init(cls):

        name = cls.__name__

        try:
            collection_type = cls.collection_type
        except:
            collection_type = 2

        try:
            cls.collection_instance = Collection.create(name=name, type=collection_type)
        except:
            cls.collection_instance = Collection.get_loaded_collection(name=name)


    def __init__(self):
        """
        """

        pass
