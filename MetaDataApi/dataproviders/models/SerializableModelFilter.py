class SerializableModelFilter:
    def __init__(self, max_depth, exclude_labels=()):
        self.current_depth = 0
        self.parrent_object_name = None
        self.max_depth = max_depth
        self.exclude_labels = exclude_labels

    def apply_filter(self, labels : list) -> list:
        if self.current_depth >= self.max_depth:
            return []
