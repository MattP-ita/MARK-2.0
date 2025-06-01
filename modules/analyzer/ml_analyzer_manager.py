import os
from typing import Type, List

from modules.analyzer.library_dict_type import LibraryDictType
from modules.analyzer.ml_analyzer import MLAnalyzer
from modules.analyzer.ml_roles import AnalyzerRole


class MLAnalyzerManager:
    _registry = {}

    def __init__(
        self,
        analyzer_class: Type['MLAnalyzer'],
        role: AnalyzerRole,
        dict_types: List[LibraryDictType],
    ):
        self.analyzer_class = analyzer_class
        self.role = role
        self.dict_types = dict_types


    @classmethod
    def register_specialization(cls, role_name: AnalyzerRole, analyzer_class: Type['MLAnalyzer'],
                                dict_types: List[LibraryDictType]):
        cls._registry[role_name] = {
            "class": analyzer_class,
            "dicts": dict_types
        }


    @classmethod
    def from_role(cls, role_name: AnalyzerRole) -> 'MLAnalyzerManager':
        if role_name not in cls._registry:
            raise ValueError(f"Specialization '{role_name}' is not registered.")
        entry = cls._registry[role_name]
        return cls(analyzer_class=entry["class"], role=role_name, dict_types=entry["dicts"])


    def analyze(self, input_path, output_path, analyzer_path, **kwargs):
        role_str = str(self.role.value)
        role_folder = os.path.join(output_path,role_str)
        os.makedirs(role_folder, exist_ok=True)
        count = len(os.listdir(role_folder))
        result_name = f"{role_str}_{count + 1}"
        output_folder = os.path.join(role_folder, result_name)
        os.makedirs(output_folder, exist_ok=True)

        dict_paths = {}
        for dict_type in self.dict_types:
            full_path = os.path.join(analyzer_path, "library_dictionary", dict_type.value)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Dictionary '{dict_type.name}' not found at: {full_path}")
            dict_paths[dict_type.name] = full_path

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input folder not found: {input_path}")

        analyzer = self.analyzer_class(output_folder=output_folder)

        print(f"Running analysis for role: {role_str}")
        print(f"Input folder: {input_path}")
        print(f"Output folder: {output_folder}")
        print(f"Dictionaries used: {dict_paths}")
        if kwargs:
            print(f"Extra analyzer arguments: {kwargs}")

        analyzer.analyze_projects_set(input_path, *dict_paths.values(), **kwargs)
        return result_name
