"""Enum definitions for supported library dictionary types."""

from enum import Enum
from pathlib import Path


class LibraryDictType(str, Enum):
    """Enumeration of available ML library dictionary file types."""

    PRODUCER = Path("./io/library_dictionary/library_dict_producers.csv")
    CONSUMER = Path("./io/library_dictionary/library_dict_consumers.csv")
