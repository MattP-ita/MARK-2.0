"""Module for filtering relevant libraries from a file based on a dictionary."""

import pandas as pd

from modules.library_manager.library_extractor import LibraryExtractor


class LibraryFilter:
    """Provides methods to load and filter libraries used in source code files."""

    @staticmethod
    def load_dict(path: str) -> pd.DataFrame:
        """Load the library dictionary from a CSV file."""
        return pd.read_csv(path, delimiter=",")

    @staticmethod
    def filter_used_libraries(file_path: str, library_dict: pd.DataFrame) -> pd.DataFrame:
        """Filter and return libraries from the file that are present in the dictionary."""
        file_libraries = LibraryExtractor.get_libraries_from_file(file_path)

        clean_libs = [
            lib.split(".")[0].strip()
            for lib in file_libraries
        ]

        return library_dict[library_dict["library"].isin(clean_libs)]
