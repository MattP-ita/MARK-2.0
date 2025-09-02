"""Facade for orchestrating ML analysis using registered analyzers by role."""

import os

from modules.analyzer.analyzer_decorator import log_and_time
from modules.analyzer.analyzer_factory import AnalyzerFactory
from modules.analyzer.ml_roles import AnalyzerRole
from modules.utils.logger import get_logger

logger = get_logger(__name__)


class MLAnalysisFacade:
    """Handles the full ML analysis workflow for a given role."""

    def __init__(self, input_path, io_path, role: AnalyzerRole):
        """Initialize the analysis facade with paths and analyzer role.

        Args:
            input_path (str): Path to the project input folder.
            io_path (str): Path to the base I/O directory (e.g., for dictionaries and output).
            role (AnalyzerRole): Role specifying the type of analysis.
        """
        self.input_path = input_path
        self.io_path = io_path
        self.role = role
        self.role_str = str(self.role.value)

    def _resolve_paths(self, dict_types):
        """Resolve paths for required dictionaries and create output folder.

        Args:
            dict_types (List[Enum]): Types of dictionaries required by the analyzer.

        Returns:
            Tuple[str, str]: result_name, output_path
        """
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(
                f"Input folder not found: {self.input_path}"
            )

        for dict_type in dict_types:
            if not os.path.exists(dict_type.value):
                raise FileNotFoundError(
                    f"Dictionary '{dict_type.name}' not found at: 'full_path'"
                )

        role_folder = os.path.join(self.io_path, "output", self.role_str)
        os.makedirs(role_folder, exist_ok=True)
        count = len(os.listdir(role_folder))
        result_name = f"{self.role_str}_{count + 1}"
        output_path = os.path.join(role_folder, result_name)
        os.makedirs(output_path, exist_ok=True)

        return result_name, output_path

    @log_and_time("MLAnalysis")
    def run_analysis(self, **kwargs):
        """Run the ML analysis using the builder registered for the current role.

        Args:
            **kwargs: Extra parameters to pass to the analyzer.

        Returns:
            str: The result folder name used for output.
        """
        analyzer = AnalyzerFactory.create_builder(self.role).build()

        result_name, output_path = self._resolve_paths(analyzer.library_dicts)

        analyzer.analyze_projects_set(self.input_path, output_path, **kwargs)

        logger.info("Running analysis for role: %s", self.role_str)
        logger.info("Input folder: %s", self.input_path)
        logger.info("Output folder: %s", output_path)
        logger.info("Dictionaries used: %s", analyzer.library_dicts)
        if kwargs:
            logger.info("Extra analyzer arguments: %s", kwargs)
        logger.info("Analysis complete. Results written to: %s", output_path)

        return result_name
