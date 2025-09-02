"""Default, regex-based keyword extraction strategy for MARK.

This module implements the concrete KeywordExtractionStrategy used by analyzers
to spot ML-related API usages inside source files. It reads a file line-by-line,
builds case-insensitive regular expressions from the KB keywords (handling dots,
parentheses, and optional whitespace), and records every match together with its
library, file path, and line number. """

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
