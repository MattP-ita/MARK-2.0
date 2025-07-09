import os

from modules.analyzer.analyzer_decorator import log_and_time
from modules.analyzer.analyzer_factory import AnalyzerFactory
from modules.analyzer.ml_roles import AnalyzerRole

from modules.utils.logger import get_logger
logger = get_logger(__name__)

class MLAnalysisFacade:
    def __init__(self, input_path, io_path, role: AnalyzerRole):
        self.input_path = input_path
        self.io_path = io_path
        self.role = role
        self.role_str = str(self.role.value)

    def _resolve_paths(self, dict_types):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input folder not found: {self.input_path}")

        dict_paths = {}
        for dict_type in dict_types:
            full_path = os.path.join(self.io_path, "library_dictionary", dict_type.value)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Dictionary '{dict_type.name}' not found at: {full_path}")
            dict_paths[dict_type.name] = full_path

        role_folder = os.path.join(self.io_path, "output", self.role_str)
        os.makedirs(role_folder, exist_ok=True)
        count = len(os.listdir(role_folder))
        result_name = f"{self.role_str}_{count + 1}"
        output_path = os.path.join(role_folder, result_name)
        os.makedirs(output_path, exist_ok=True)

        return result_name, output_path, dict_paths

    @log_and_time("MLAnalysis")
    def run_analysis(self, **kwargs):
        builder = AnalyzerFactory.create_builder(self.role)

        result_name, output_path, dict_paths = self._resolve_paths(builder.required_dict_types)

        analyzer = (
            builder
            .with_output_folder(output_path)
            .build()
        )

        analyzer.analyze_projects_set(self.input_path, *dict_paths.values(), **kwargs)

        logger.info(f"Running analysis for role: {self.role_str}")
        logger.info(f"Input folder: {self.input_path}")
        logger.info(f"Output folder: {output_path}")
        logger.info(f"Dictionaries used: {dict_paths}")
        if kwargs:
            logger.info(f"Extra analyzer arguments: {kwargs}")
        logger.info(f"Analysis complete. Results written to: {output_path}")
        return result_name
