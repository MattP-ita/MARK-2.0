from modules.scanner.file_filter.file_filter_base import FileFilter

class ExtensionFilter(FileFilter):

    def __init__(self, extensions):
        self.extensions = extensions

    def accept(self, file_name: str) -> bool:
        return any(file_name.endswith(ext) for ext in self.extensions)