from modules.analyzer.builder.analyzer_builder import AnalyzerBuilder
from modules.analyzer.builder.register_builder import register_builder
from modules.analyzer.ml_producer_analyzer import MLProducerAnalyzer
from modules.analyzer.ml_roles import AnalyzerRole
from modules.keyword_extractor.keyword_extractor_default import DefaultKeywordMatcher
from modules.library_manager.library_dict_type import LibraryDictType
from modules.scanner.file_filter.extension_filter import ExtensionFilter
from modules.scanner.project_scanner import ProjectScanner


@register_builder(AnalyzerRole.PRODUCER)
class ProducerAnalyzerBuilder(AnalyzerBuilder):
    def __init__(self):
        super().__init__()
        self.with_role(AnalyzerRole.PRODUCER)
        self.with_analyzer_class(MLProducerAnalyzer)
        self.with_library_dicts([LibraryDictType.PRODUCER])
        self.with_scanner(ProjectScanner(filters=[ExtensionFilter([".py", ".ipynb"])]))
        self.with_keyword_strategy(DefaultKeywordMatcher())
