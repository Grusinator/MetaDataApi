class BaseDescriptor(object):

    def __init__(self, meta_type):
        self.meta_type = meta_type

    def __set_name__(self, owner, name):
        self.label = name

    def create_schema_object(self):
        pass
