import re

from modules.scanner.file_filter.file_filter_base import FileFilter


class ExcludeTestFilesFilter(FileFilter):

    def accept(self, file_name: str) -> bool:
        return not re.search(r"test|example|eval|validat", file_name, re.IGNORECASE)