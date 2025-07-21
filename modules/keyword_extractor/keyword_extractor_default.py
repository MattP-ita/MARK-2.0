"""Keyword extraction strategy using default regex-based matching."""

import re
from modules.keyword_extractor.keyword_extractor_base import KeywordExtractionStrategy
from modules.utils.logger import get_logger

logger = get_logger(__name__)


class DefaultKeywordMatcher(KeywordExtractionStrategy):
    """Default implementation of keyword extraction using regex pattern matching."""

    def extract_keywords(self, file, related_dict):
        """Extract keywords from the file based on the provided keyword dictionary."""
        matches = []

        try:
            with open(file, "r", encoding="utf-8") as f:
                for line_number, line in enumerate(f, 1):
                    for _, row in related_dict.iterrows():
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
            logger.error("Error reading file %s", file)
        except FileNotFoundError:
            logger.error("Error finding file %s", file)

        return matches

    @staticmethod
    def build_regex(keyword):
        """Build a regex pattern from a keyword with optional escaping."""
        if '.' in str(keyword):
            keyword = keyword.replace('.', r'\.')

        if r'\s' in str(keyword):
            parts = keyword.split()
            regex = r'\s*'.join(parts)
            return re.compile(regex, re.IGNORECASE)

        if '(' in str(keyword):
            keyword = keyword.replace('(', r'\(')

        return re.compile(str(keyword), re.IGNORECASE)
