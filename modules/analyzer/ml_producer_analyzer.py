"""Analyzer for detecting ML usage by producer libraries."""

from modules.library_manager.library_filter import LibraryFilter
from modules.analyzer.ml_analyzer import MLAnalyzer


class MLProducerAnalyzer(MLAnalyzer):
    """Analyzer for identifying ML activity related to producer libraries."""

    def check_methods(self, file, producer_library, **kwargs):
        """Check ML usage in a file using only the producer library."""
        list_load_keywords = []
        keywords = []

        library_dict = LibraryFilter.load_dict(producer_library)
        related_dict = LibraryFilter.filter_used_libraries(file, library_dict)
        libraries = related_dict['library'].tolist()

        if not libraries:
            return libraries, keywords, list_load_keywords

        keywords = self.keyword_strategy.extract_keywords(file, related_dict)

        return libraries, keywords, list_load_keywords
