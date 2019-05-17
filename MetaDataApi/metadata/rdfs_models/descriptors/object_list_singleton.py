class ObjectListSingleton:
    __object_instance_list = None

    @staticmethod
    def getInstance(name):
        """ Static access method. """
        if ObjectListSingleton.__object_instance_list == None:
            ObjectListSingleton()
        return ObjectListSingleton.__object_instance_list

    def __init__(self):
        """ Virtually private constructor. """
        if ObjectListSingleton.__object_instance_list != None:
            raise Exception("This class is a singleton!")
        else:
            ObjectListSingleton.__object_instance_list = self
