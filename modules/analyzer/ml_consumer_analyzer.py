"""Module implementing MLConsumerAnalyzer for analyzing consumer ML usage."""

from modules.library_manager.library_filter import LibraryFilter
from modules.analyzer.ml_analyzer import MLAnalyzer

from modules.utils.logger import get_logger
logger = get_logger(__name__)


class MLConsumerAnalyzer(MLAnalyzer):
    """Analyzer for detecting ML usage by consumer libraries."""

    def check_training_method(self, file, producer_library):
        """Check if a file uses training methods from a producer library."""
        library_dict = LibraryFilter.load_dict(producer_library)
        related_dict = LibraryFilter.filter_used_libraries(file, library_dict)
        libraries = related_dict['library'].tolist()

        if not libraries:
            return False
        try:
            with open(file, "r", encoding="utf-8") as f:
                file_content = f.read()
                for _, row in related_dict.iterrows():
                    keyword = row['Keyword']
                    if keyword in file_content:
                        return True
        except UnicodeDecodeError:
            logger.error("Error reading file %s", file)
        except FileNotFoundError:
            logger.error("Error finding file %s", file)

        return False

    def check_library(self, file, consumer_library, producer_library, rules_3, **kwargs):
        """Override check_library for MLConsumerAnalyzer """
        list_load_keywords = []
        keywords = []

        library_dict = LibraryFilter.load_dict(consumer_library)
        related_dict = LibraryFilter.filter_used_libraries(file, library_dict)
        libraries = related_dict['library'].tolist()

        if not libraries:
            return libraries, keywords, list_load_keywords

        if rules_3 and self.check_training_method(file, producer_library):
            return libraries, keywords, list_load_keywords

        keywords = self.keyword_strategy.extract_keywords(file, related_dict)

        return libraries, keywords, list_load_keywords
