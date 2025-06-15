from modules.library_manager.library_filter import LibraryFilter
from modules.analyzer.ml_analyzer import MLAnalyzer


class MLProducerAnalyzer(MLAnalyzer):

    def check_methods(self, file, producer_library, **kwargs):
        list_load_keywords = []
        keywords = []

        library_dict = LibraryFilter.load_dict(producer_library)
        related_dict = LibraryFilter.filter_used_libraries(file, library_dict)
        libraries = related_dict['library'].tolist()

        if not libraries:
            return libraries, keywords, list_load_keywords

        keywords = self.keyword_strategy.extract_keywords(file, related_dict)

        return libraries, keywords, list_load_keywords