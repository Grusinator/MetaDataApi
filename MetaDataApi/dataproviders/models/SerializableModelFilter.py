class SerializableModelFilter:
    DEPTH_INFINITE = 999999
    DEPTH_TEMP_FIX_D1 = 2

    def __init__(self, max_depth, exclude_labels=()):
        self.current_depth = 0
        self.parrent_object_name = None
        self.max_depth = max_depth
        self.exclude_labels = exclude_labels

    def apply_filter(self, labels : list) -> list:
        if self.current_depth >= self.max_depth:
            return []

    @classmethod
    def adjust_depth(cls, depth):
        if depth == cls.DEPTH_INFINITE:
            return depth
        else:
            return depth - 1 if depth > 0 else 0
