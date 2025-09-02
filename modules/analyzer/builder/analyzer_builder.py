"""Define a builder for constructing ML analyzers with consistent configurations.
This abstract component collects all required dependencies (analysis role, file filters, keyword-extraction strategy,
and library dictionary types) and produces a ready-to-use analyzer instance only when the configuration is complete.

By centralizing setup in a single place, it eliminates scattered initialization code, reduces duplication,
and prevents partially configured objects. Concrete builders specify the analyzer class to instantiate and may
be discovered/registered by the Factory–Registry mechanism.

The goal is to decouple “how an analyzer is assembled”
from “how it is used,” improving readability, testability, and extensibility of the analysis pipeline."""

from abc import ABC
from typing import List, Optional

from modules.analyzer.ml_roles import AnalyzerRole
from modules.library_manager.library_dict_type import LibraryDictType
from modules.scanner.file_filter.file_filter_base import FileFilter


class AnalyzerBuilder(ABC):
    """Builder class for constructing MLAnalyzer instances step-by-step."""

    def __init__(self):
        """Initialize builder with default values."""
        self._role = None
        self._filters = None
        self._keyword_strategy = None
        self._dict_types = []
        self._analyzer_class = None

    def with_role(self, role: AnalyzerRole):
        """Set the ML analysis role (producer/consumer)."""
        self._role = role
        return self

    def with_filters(self, filters: Optional[List[FileFilter]] = None):
        """Set the scanner used to extract project files."""
        self._filters = filters or []
        return self

    def with_keyword_strategy(self, strategy):
        """Set the keyword extraction strategy."""
        self._keyword_strategy = strategy
        return self

    def with_library_dicts(self, dict_types: List[LibraryDictType]):
        """Set the required library dictionary types."""
        self._dict_types = dict_types
        return self

    def with_analyzer_class(self, cls):
        """Optionally override the analyzer class to instantiate."""
        self._analyzer_class = cls
        return self

    def build(self):
        """Build and return the configured MLAnalyzer instance."""
        if not all([self._role, self._filters, self._keyword_strategy]):
            raise ValueError("Missing required parameters to build analyzer")

        if self._analyzer_class is None:
            raise ValueError("Analyzer class must be set with `with_analyzer_class()`")

        analyzer = self._analyzer_class(
            role=self._role,
            library_dicts= self._dict_types,
            filters=self._filters,
            keyword_strategy=self._keyword_strategy
        )

        return analyzer
