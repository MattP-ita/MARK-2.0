"""Analyzer specialization for ML consumers.

This module provides the MLConsumerAnalyzer, a concrete subclass of MLAnalyzer that applies the consumer rules over
source files. It loads the consumer and producer library dictionaries, filters used libraries in a file,
and (optionally)enforces the “no training APIs” constraint (Rule 3) by consulting the producer dictionary
before accepting a match. Keyword extraction is delegated to the configured strategy."""

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

    def check_library(self, file, **kwargs):
        """Override check_library for MLConsumerAnalyzer """
        consumer_library = self.library_dicts[0]
        producer_library = self.library_dicts[1]
        rules_3 = kwargs.get("rules_3", False)

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
