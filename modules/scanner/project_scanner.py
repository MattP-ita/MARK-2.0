import os
from typing import List, Optional

from modules.analyzer.notebook_converter import NotebookConverter
from modules.scanner.file_filter.file_filter_base import FileFilter
from modules.utils.logger import get_logger

logger = get_logger(__name__)


class ProjectScanner:
    def __init__(
        self,
        filters: Optional[List[FileFilter]] = None,
        notebook_converter: Optional[NotebookConverter] = None
    ):
        self.filters = filters or []
        self.notebook_converter = notebook_converter or NotebookConverter()

    def is_valid_file(self, filename: str) -> bool:
        return all(file_filter.accept(filename) for file_filter in self.filters)

    def scan(self, repo_path: str) -> List[str]:
        if not os.path.isdir(repo_path):
            logger.error("The specified directory does not exist: %s", repo_path)
            raise FileNotFoundError(f"The specified directory does not exist: {repo_path}")

        logger.info("Starting scan of repository: %s", repo_path)

        collected_files = []

        for root, dirs, files in os.walk(repo_path):
            for filename in files:
                if not self.is_valid_file(filename):
                    logger.debug("File excluded by filters: %s", filename)
                    continue

                file_path = os.path.join(root, filename)

                if filename.endswith(".ipynb"):
                    try:
                        file_path = self.notebook_converter.convert_notebook_to_code(file_path)
                        logger.info(f"Converted: {filename} -> {file_path}")
                        logger.info("Notebook converted successfully: %s", file_path)
                    except Exception as e:
                        logger.error("Failed to convert notebook %s: %s", filename, str(e))
                        continue

                collected_files.append(file_path)

        logger.info("Total valid files collected: %d", len(collected_files))
        return collected_files
