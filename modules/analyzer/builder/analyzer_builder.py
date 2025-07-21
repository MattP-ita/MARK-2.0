"""Defines the abstract builder pattern for ML analyzers."""

from abc import ABCMeta
from typing import List

from modules.analyzer.ml_roles import AnalyzerRole
from modules.library_manager.library_dict_type import LibraryDictType
from modules.scanner.project_scanner import ProjectScanner


class AnalyzerBuilder(metaclass=ABCMeta):
    """Builder class for constructing MLAnalyzer instances step-by-step."""

    def __init__(self):
        """Initialize builder with default values."""
        self._output_folder = None
        self._role = None
        self._scanner = None
        self._keyword_strategy = None
        self._dict_types = []
        self._analyzer_class = None

    def with_output_folder(self, path):
        """Set the output folder for the analyzer."""
        self._output_folder = path
        return self

    def with_role(self, role: AnalyzerRole):
        """Set the ML analysis role (producer/consumer)."""
        self._role = role
        return self

    def with_scanner(self, scanner: ProjectScanner):
        """Set the scanner used to extract project files."""
        self._scanner = scanner
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

    @property
    def required_dict_types(self):
        """Get the list of required library dictionary types."""
        return self._dict_types

    def build(self):
        """Build and return the configured MLAnalyzer instance."""
        if not all([self._output_folder, self._role, self._scanner]):
            raise ValueError("Missing required parameters to build analyzer")

        if self._analyzer_class is None:
            raise ValueError("Analyzer class must be set with `with_analyzer_class()`")

        analyzer = self._analyzer_class(
            output_folder=self._output_folder,
            role=self._role,
            scanner=self._scanner,
            keyword_strategy=self._keyword_strategy
        )

        return analyzer
