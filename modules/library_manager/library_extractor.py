"""Lightweight utility to parse source files and extract imported libraries.

This module exposes a helper that reads a source file
and collects module names referenced by import ... and from ... import ...
statements. It returns a normalized list of imported identifiers without resolving
dependencies or executing code. Errors (e.g., unreadable files or unsupported
encodings) are logged via the global logger and handled gracefully, making the
extractor safe to use across large codebases."""

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
