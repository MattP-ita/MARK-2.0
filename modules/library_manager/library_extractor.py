"""Module for extracting and checking imported libraries from source code files."""

from modules.utils.logger import get_logger

logger = get_logger(__name__)


class LibraryExtractor:
    """Utility class for extracting library imports and checking ML library usage."""

    @staticmethod
    def get_libraries_from_file(file_path: str) -> list:
        """Extract a list of libraries imported in a given source file."""
        libraries = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="ISO-8859-1") as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                logger.error("Error reading file %s", file_path)
                return libraries
        except FileNotFoundError:
            logger.error("Error finding file %s", file_path)
            return libraries

        for line in lines:
            line = line.lstrip()
            if "import " in line:
                if "from" in line:
                    libraries.append(line.split(" ")[1])
                else:
                    libraries.append(line.split(" ")[1])
        return libraries

    @staticmethod
    def check_ml_library_usage(file_path: str, library_dict):
        """Filter and return ML libraries used in a file from the provided dictionary."""
        file_libraries = LibraryExtractor.get_libraries_from_file(file_path)
        for i, lib in enumerate(file_libraries):
            if "." in lib:
                file_libraries[i] = lib.split(".")[0]
        dict_libraries = library_dict[library_dict["library"].isin(file_libraries)]
        return dict_libraries
