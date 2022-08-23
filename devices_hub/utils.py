from enum import Enum


class ListEnum(Enum):
    @classmethod
    def list(cls):
        return [el.value for el in cls]
