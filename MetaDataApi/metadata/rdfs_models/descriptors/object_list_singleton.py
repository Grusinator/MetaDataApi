class RdfsModelInitializedList:
    _list = []

    @staticmethod
    def get_by_name(label):
        model = next((x for x in RdfsModelInitializedList._list if type(x).__name__ == label), None)
        if model is None:
            raise ModelNotInitializedException("cant create from name, yet")
            # model = DefaultRdfsObjectFactory.getObject()
            # RdfsModelInitializedList._list.append(model)
        return model

    @staticmethod
    def set(model):
        from MetaDataApi.metadata.rdfs_models.base_rdfs_object import BaseRdfsModel
        if not issubclass(model, BaseRdfsModel):
            raise TypeError("this is not a RdfsModel")
        if model not in RdfsModelInitializedList._list:
            RdfsModelInitializedList._list.append(model)


class ModelNotInitializedException(Exception):
    pass
