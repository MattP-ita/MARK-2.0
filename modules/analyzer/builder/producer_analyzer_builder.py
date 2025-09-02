"""Defines the builder for the ML producer analyzer."""

from modules.analyzer.analyzer_factory import AnalyzerFactory
from modules.analyzer.builder.analyzer_builder import AnalyzerBuilder
from modules.analyzer.ml_producer_analyzer import MLProducerAnalyzer
from modules.analyzer.ml_roles import AnalyzerRole
from modules.keyword_extractor.keyword_extractor_default import DefaultKeywordMatcher
from modules.library_manager.library_dict_type import LibraryDictType
from modules.scanner.file_filter.extension_filter import ExtensionFilter


@AnalyzerFactory.register(AnalyzerRole.PRODUCER)
class ProducerAnalyzerBuilder(AnalyzerBuilder):
    """Concrete builder for ML producer analyzers,
    pre-configured with role, scanner, and strategy.
    """

    def __init__(self):
        super().__init__()
        self.with_role(AnalyzerRole.PRODUCER)
        self.with_analyzer_class(MLProducerAnalyzer)
        self.with_library_dicts([LibraryDictType.PRODUCER])
        self.with_filters([ExtensionFilter([".py"])])
        self.with_keyword_strategy(DefaultKeywordMatcher())
