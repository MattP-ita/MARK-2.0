"""Module for scanning project directories and collecting valid source files."""

from typing import List, Optional

from modules.scanner.file_filter.file_filter_base import FileFilter
from modules.utils.logger import get_logger

logger = get_logger(__name__)


class ProjectScanner:
    """Scans project folders to collect source files that match given filter criteria."""

    @staticmethod
    def is_valid_file(filename: str, filters: List[FileFilter]) -> bool:
        """
        Check whether the given file is accepted by all configured filters.
        """
        return all(file_filter.accept(filename) for file_filter in filters)
