import logging

logger = logging.getLogger(__name__)

class SerializableModelFilter:
    DEPTH_INFINITE = 999999

    def __init__(self, max_depth=DEPTH_INFINITE, exclude_labels=(), start_object_name=None):
        self.current_depth = 0
        self.ancestors = []
        self.parrent_object_name = None
        self.current_object_name = start_object_name
        if self.current_object_name is None:
            logger.warning("starting object has not been set which could lead to issues")
        self.max_depth = max_depth
        self.exclude_labels = exclude_labels

    def apply_relation_filter(self, labels: list) -> list:
        if self.is_max_depth_reached():
            return []
        labels = self.remove_parrent_object(labels)
        labels = self.remove_exclude_labels(labels)
        return labels

    def apply_property_filter(self, labels: list) -> list:
        labels = self.remove_exclude_labels(labels)
        return labels

    def is_max_depth_reached(self):
        return self.current_depth == self.max_depth

    def remove_parrent_object(self, labels: list):
        try:
            labels.remove(self.parrent_object_name)
        except ValueError:
            pass
        return labels

    def remove_exclude_labels(self, labels):
        labels = list(set(labels) - set(self.exclude_labels))
        return labels

    def step_into(self, object_name):
        logger.debug(f"adding serializer {object_name}")
        self.ancestors.append(self.parrent_object_name)
        self.parrent_object_name = self.current_object_name
        self.current_object_name = object_name
        self.current_depth += 1
        self.validate_depth()

    def step_out(self):
        self.current_object_name = self.parrent_object_name
        self.parrent_object_name = self.ancestors.pop()
        self.current_depth -= 1
        self.validate_depth()

    def validate_depth(self):
        if self.current_depth > self.max_depth:
            raise StopIteration("Something is wrong. current depth should not exceed max dept")

    @classmethod
    def adjust_depth(cls, depth):
        if depth == cls.DEPTH_INFINITE:
            return depth
        else:
            return depth - 1 if depth > 0 else 0
