"""Abstract base class for file filters used in project scanning."""

from abc import ABC, abstractmethod


class FileFilter(ABC):
    """
    Abstract base class for file filtering strategies.
    """

    @abstractmethod
    def accept(self, file_name: str) -> bool:
        """
        Determine whether the file should be accepted based on its name.

        Args:
            file_name (str): Name of the file to evaluate.

        Returns:
            bool: True if the file is accepted, False otherwise.
        """
