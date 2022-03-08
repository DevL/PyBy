from collections import UserDict
from .enumerable import Enumerable
from .enumerable_list import EnumerableList


class EnumerableDict(Enumerable, UserDict):
    def each(self, func=None):
        if func:
            for item in self.items():
                func(item)
        else:
            return iter(self.items())

    def _return_type(self):
        return EnumerableList
