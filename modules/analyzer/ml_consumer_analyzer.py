from modules.library_manager.library_filter import LibraryFilter
from modules.analyzer.ml_analyzer import MLAnalyzer
from modules.utils.logger import get_logger
logger = get_logger(__name__)


class MLConsumerAnalyzer(MLAnalyzer):

    def check_training_method(self, file, producer_library):
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
            logger.warning(f"Error reading file {file}")
        except FileNotFoundError:
            logger.warning(f"Error finding file {file}")

        return False



    def check_methods(self, file, consumer_library, producer_library, rules_3, **kwargs):
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