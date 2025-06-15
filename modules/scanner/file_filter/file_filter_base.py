import re
from abc import ABC, abstractmethod


class FileFilter(ABC):

    @abstractmethod
    def accept(self, file_name: str) -> bool:
        pass
