"""Module for converting Jupyter notebooks to Python scripts."""

import os

from modules.utils.logger import get_logger

logger = get_logger(__name__)


class NotebookConverter:
    """Provides utilities for converting .ipynb notebooks to .py scripts."""

    @staticmethod
    def convert_notebook_to_code(file_path: str) -> str:
        """Convert a single Jupyter notebook to a Python script."""
        os.system(f'jupyter nbconvert --to script "{file_path}"')
        return file_path.replace(".ipynb", ".py")

    @staticmethod
    def convert_and_check(file_path: str) -> bool:
        """Convert a notebook and check if the resulting .py file exists."""
        file_py = NotebookConverter.convert_notebook_to_code(file_path)
        return os.path.exists(file_py)

    @staticmethod
    def convert_all_notebooks(folder_path: str) -> list:
        """Convert all .ipynb notebooks in a folder (recursively)."""
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"The folder {folder_path} does not exist.")

        converted_files = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.ipynb'):
                    full_path = os.path.join(root, file)
                    try:
                        converted_file = NotebookConverter.convert_notebook_to_code(full_path)
                        converted_files.append(converted_file)
                    except Exception as e:
                        logger.error("Error converting %s: %s", full_path, e)

        return converted_files
