import re

from modules.keyword_extractor.keyword_extractor_base import KeywordExtractionStrategy
from modules.utils.logger import get_logger
logger = get_logger(__name__)


class DefaultKeywordMatcher(KeywordExtractionStrategy):
    def extract_keywords(self, file, keyword_dict):
        matches = []

        try:
            with open(file, "r", encoding="utf-8") as f:
                for line_number, line in enumerate(f, 1):
                    for _, row in keyword_dict.iterrows():
                        keyword = row['Keyword']
                        library = row['library']
                        pattern = self.build_regex(keyword)

                        if re.search(pattern, line):
                            keyword = keyword.replace("\\", "")
                            matches.append({
                                'keyword': keyword,
                                'library': library,
                                'file': file,
                                'line': line.strip(),
                                'line_number': line_number
                            })
        except UnicodeDecodeError:
            logger.error(f"Error reading file {file}")
        except FileNotFoundError:
            logger.error(f"Error finding file {file}")

        return matches

    @staticmethod
    def build_regex(keyword):
        if '.' in str(keyword):
            keyword = keyword.replace('.', '\.')
        if '\s' in str(keyword):
            parts = keyword.split()
            regex = r'\s*'.join(parts)
            return re.compile(regex, re.IGNORECASE)
        else:
            if '(' in str(keyword):
                keyword = keyword.replace('(', '\(')
            return re.compile(str(keyword), re.IGNORECASE)
