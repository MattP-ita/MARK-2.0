from enum import Enum

class LibraryDictType(str, Enum):
    PRODUCER = "library_dict_producers.csv"
    CONSUMER = "library_dict_consumers.csv"
