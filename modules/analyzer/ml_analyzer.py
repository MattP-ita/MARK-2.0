import os
import time
import pandas as pd

from modules.keyword_extractor.keyword_extractor_base import KeywordExtractionStrategy
from modules.keyword_extractor.keyword_extractor_default import DefaultKeywordMatcher
from abc import ABC, abstractmethod

from modules.analyzer.ml_roles import AnalyzerRole
from modules.scanner.project_scanner import ProjectScanner

from modules.utils.logger import get_logger
logger = get_logger(__name__)

class MLAnalyzer(ABC):

    def __init__(self, output_folder, role: AnalyzerRole , scanner: ProjectScanner, keyword_strategy: KeywordExtractionStrategy = None):
        self.output_folder = output_folder
        self.role = role
        self.role_str = str(self.role.value)
        self.scanner = scanner
        self.keyword_strategy = keyword_strategy or DefaultKeywordMatcher()
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

    def analyze_single_file(self, file, repo,  *args, **kwargs):
        libraries = []
        keywords = []
        list_load_keywords = []
        if file:
            libraries, keywords, list_load_keywords = self.check_methods(file, *args, **kwargs)
            if len(keywords) > 0:
                logger.info(f"Found {file} with ML libraries{libraries} and training instruction {keywords} in {repo}")
                return libraries, keywords, list_load_keywords
            return libraries, keywords, list_load_keywords
        return libraries, keywords, list_load_keywords

    def analyze_project(self, repo_contents, project, directory, *args, **kwargs):
        df = pd.DataFrame(columns=self.dataframe_columns)
        collected_files = self.scanner.scan(repo_contents)

        for file_path in collected_files:
            libraries, keywords, list_load_keywords = self.analyze_single_file(file_path, repo_contents,
                                                                               *args, **kwargs)
            if keywords:
                for keyword in keywords:
                    df = pd.concat([
                        df,
                        pd.DataFrame({
                            'ProjectName': f'{project}/{directory}',
                            f'Is ML {self.role_str}': 'Yes',
                            'libraries': keyword['library'],
                            'where': file_path,
                            'keyword': keyword['keyword'],
                            'line_number': keyword['line_number']
                        }, index=[0])
                    ], ignore_index=True)

        output_file = os.path.join(self.output_folder, f'{project}_{directory}_ml_{self.role_str}.csv')

        if not df.empty:
            df.to_csv(output_file, index=False)
        return df

    def analyze_projects_set(self, input_folder, *args, **kwargs):
        results_file = os.path.join(self.output_folder, 'results.csv')
        df = pd.read_csv(results_file)

        for project in os.listdir(input_folder):
            if not os.path.isdir(os.path.join(input_folder, project)):
                continue

            for dir_path in os.listdir(os.path.join(input_folder, project)):
                logger.info("Project:", project)
                if os.path.isdir(os.path.join(input_folder, project, dir_path)):
                    new_df = self.analyze_project(
                        os.path.join(input_folder, project, dir_path),
                        project,
                        dir_path,
                        *args, **kwargs
                    )
                    df = pd.concat([df, new_df], ignore_index=True)
                    df.to_csv(results_file, index=False)

        return df

    @abstractmethod
    def check_methods(self, *args, **kwargs):
        pass

    @property
    def dataframe_columns(self):
        return ['ProjectName', f'Is ML {self.role_str}', 'libraries', "where", "keywords", 'line_number']