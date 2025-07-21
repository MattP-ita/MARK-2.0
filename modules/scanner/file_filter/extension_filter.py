"""File filter that accepts files based on their extensions."""

from modules.scanner.file_filter.file_filter_base import FileFilter


class ExtensionFilter(FileFilter):
    """
    A filter that accepts files matching specific extensions.
    """

    def __init__(self, extensions):
        """
        Initialize the ExtensionFilter.

        Args:
            extensions (list): List of allowed file extensions (e.g., [".py", ".ipynb"]).
        """
        self.extensions = extensions

    def accept(self, file_name: str) -> bool:
        """
        Check whether the file name ends with one of the allowed extensions.

        Args:
            file_name (str): The name of the file to check.

        Returns:
            bool: True if the file matches one of the allowed extensions, False otherwise.
        """
        return any(file_name.endswith(ext) for ext in self.extensions)
