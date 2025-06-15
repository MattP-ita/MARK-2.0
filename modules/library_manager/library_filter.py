import pandas as pd

from modules.library_manager.library_extractor import LibraryExtractor


class LibraryFilter:
    @staticmethod
    def load_dict(path: str) -> pd.DataFrame:
        return pd.read_csv(path, delimiter=",")

    @staticmethod
    def filter_used_libraries(file_path: str, library_dict: pd.DataFrame) -> pd.DataFrame:
        file_libraries = LibraryExtractor.get_libraries_from_file(file_path)

        clean_libs = [
            lib.split(".")[0].strip()
            for lib in file_libraries
        ]

        return library_dict[library_dict['library'].isin(clean_libs)]
