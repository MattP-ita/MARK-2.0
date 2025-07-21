"""Enum definitions for supported library dictionary types."""

from enum import Enum


class LibraryDictType(str, Enum):
    """Enumeration of available ML library dictionary file types."""

    PRODUCER = "library_dict_producers.csv"
    CONSUMER = "library_dict_consumers.csv"
