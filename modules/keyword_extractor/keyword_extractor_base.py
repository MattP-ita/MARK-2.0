"""Defines the base interface for keyword extraction strategies."""

from abc import ABC, abstractmethod


class KeywordExtractionStrategy(ABC):
    """Abstract base class for keyword extraction from source files."""

    @abstractmethod
    def extract_keywords(self, file: str, related_dict) -> list[dict]:
        """
        Extract keywords from a file using the provided related dictionary.

        Args:
            file (str): Path to the file to analyze.
            related_dict: A filtered dictionary of relevant keywords/libraries.

        Returns:
            list[dict]: A list of extracted keyword data, each represented as a dictionary.
        """
