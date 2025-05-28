import os
import re
import time
from modules.analyzer.library_extractor import LibraryExtractor
from abc import ABC, abstractmethod

import pandas as pd


class MLAnalyzer(ABC):

    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.init_analysis_folder()


    def init_analysis_folder(self):
        consumer_analysis_path = os.path.join(self.output_folder, "analysis")
        if not os.path.exists(consumer_analysis_path):
            os.makedirs(consumer_analysis_path)

        results_file = os.path.join(self.output_folder, 'results.csv')
        if not os.path.exists(results_file):
            df = pd.DataFrame(columns=self.dataframe_columns)
            df.to_csv(results_file, index=False)
        else:
            df = pd.read_csv(results_file)
            df.to_csv(os.path.join(self.output_folder, f'results_backup_{int(time.time())}.csv'), index=False)



    @abstractmethod
    def check_training_method(self, file, producer_library):
        pass

    @abstractmethod
    def analyze_single_file(self, *args, **kwargs):
        pass

    @abstractmethod
    def analyze_project(self, *args, **kwargs):
        pass

    @abstractmethod
    def analyze_projects_set(self, *args, **kwargs):
        pass

    @staticmethod
    def baseline_check(project, dir, df):
        return f"{project}/{dir}" in df['ProjectName'].values

    @property
    @abstractmethod
    def dataframe_columns(self):
        pass

    @staticmethod
    def load_library_dict(input_file):
        return pd.read_csv(input_file, delimiter=",")

    @staticmethod
    def build_regex_pattern(keyword):
        keyword = re.escape(keyword)
        keyword = keyword.replace(r"\ ", r"\\s*")
        return re.compile(keyword, re.IGNORECASE)

    @staticmethod
    def check_ml_library_usage(file, library_dict):
        file_libraries = LibraryExtractor.get_libraries_from_file(file)
        for i in range(len(file_libraries)):
            if "." in file_libraries[i]:
                file_libraries[i] = file_libraries[i].split(".")[0]
            file_libraries[i] = file_libraries[i].replace("\n", "")
        # filter dict libraries from file libraries
        dict_libraries = library_dict[library_dict['library'].isin(file_libraries)]

        return dict_libraries