import pandas as pd
import os

from modules.analyzer.library_dict_type import LibraryDictType


class LibraryDictManager:

    def __init__(self, analyzer_path):
        self.analyzer_path = analyzer_path
        self.dict_dir = os.path.join(analyzer_path, "library_dictionary")

    def update_dictionary(self, dict_type: LibraryDictType, new_entries_path: str) -> int:
        dict_path = os.path.join(self.dict_dir, dict_type.value)

        if not os.path.exists(dict_path):
            raise FileNotFoundError(f"Dictionary file not found: {dict_path}")
        if not os.path.exists(new_entries_path):
            raise FileNotFoundError(f"New entries file not found: {new_entries_path}")

        existing_df = pd.read_csv(dict_path)
        new_entries_df = pd.read_csv(new_entries_path)

        key_columns = ["library", "Keyword", "ML_Category", "Link"]

        existing_df = existing_df[key_columns]
        new_entries_df = new_entries_df[key_columns]

        new_entries_df = new_entries_df.drop_duplicates()

        merged_df = pd.concat([existing_df, new_entries_df])
        merged_df = merged_df.drop_duplicates()
        merged_df = merged_df.sort_values(by=key_columns, key=lambda col: col.str.lower() if col.dtype == "object" else col)


        added_rows = len(merged_df) - len(existing_df)

        merged_df.to_csv(dict_path, index=False)
        return added_rows
