"""File filter that excludes test, example, eval, and validation-related files."""

import re

from modules.scanner.file_filter.file_filter_base import FileFilter


class ExcludeTestFilesFilter(FileFilter):
    """
    A filter that excludes files typically associated with tests, examples,
    evaluations, or validations based on filename patterns.
    """

    def accept(self, file_name: str) -> bool:
        """
        Check whether the file name should be accepted (i.e., not a test or example file).

        Args:
            file_name (str): The name of the file to check.

        Returns:
            bool: True if the file is acceptable, False if it should be excluded.
        """
        return not re.search(r"test|example|eval|validat", file_name, re.IGNORECASE)
