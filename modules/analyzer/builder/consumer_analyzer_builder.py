"""Defines the builder for the ML consumer analyzer."""

from modules.analyzer.analyzer_factory import AnalyzerFactory
from modules.analyzer.builder.analyzer_builder import AnalyzerBuilder
from modules.analyzer.ml_consumer_analyzer import MLConsumerAnalyzer
from modules.analyzer.ml_roles import AnalyzerRole
from modules.keyword_extractor.keyword_extractor_default import DefaultKeywordMatcher
from modules.library_manager.library_dict_type import LibraryDictType
from modules.scanner.file_filter.exclude_test_files import ExcludeTestFilesFilter
from modules.scanner.file_filter.extension_filter import ExtensionFilter


@AnalyzerFactory.register(AnalyzerRole.CONSUMER)
class ConsumerAnalyzerBuilder(AnalyzerBuilder):
    """Concrete builder for ML consumer analyzers, pre-configured with filters and roles."""

    def __init__(self):
        super().__init__()
        self.with_role(AnalyzerRole.CONSUMER)
        self.with_analyzer_class(MLConsumerAnalyzer)
        self.with_library_dicts([LibraryDictType.CONSUMER, LibraryDictType.PRODUCER])
        self.with_filters([
            ExtensionFilter([".py"]),
            ExcludeTestFilesFilter()
        ])
        self.with_keyword_strategy(DefaultKeywordMatcher())
