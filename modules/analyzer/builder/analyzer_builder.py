from typing import List

from modules.analyzer.ml_analyzer import MLAnalyzer
from modules.analyzer.ml_roles import AnalyzerRole
from modules.library_manager.library_dict_type import LibraryDictType
from modules.scanner.project_scanner import ProjectScanner


class AnalyzerBuilder:
    def __init__(self):
        self._output_folder = None
        self._role = None
        self._scanner = None
        self._keyword_strategy = None
        self._dict_types = []
        self._analyzer_class = MLAnalyzer

    def with_output_folder(self, path):
        self._output_folder = path
        return self

    def with_role(self, role: AnalyzerRole):
        self._role = role
        return self

    def with_scanner(self, scanner: ProjectScanner):
        self._scanner = scanner
        return self

    def with_keyword_strategy(self, strategy):
        self._keyword_strategy = strategy
        return self

    def with_library_dicts(self, dict_types: List[LibraryDictType]):
        self._dict_types = dict_types
        return self

    def with_analyzer_class(self, cls):
        self._analyzer_class = cls
        return self

    @property
    def required_dict_types(self):
        return self._dict_types

    def build(self):
        if not all([self._output_folder, self._role, self._scanner]):
            raise ValueError("Missing required parameters to build analyzer")

        analyzer = self._analyzer_class(
            output_folder=self._output_folder,
            role=self._role,
            scanner=self._scanner,
            keyword_strategy = self._keyword_strategy
        )

        return analyzer
