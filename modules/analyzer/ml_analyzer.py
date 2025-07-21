"""Abstract base class for ML analyzers handling project scans and keyword detection."""

import os
import time
from abc import ABC, abstractmethod

import pandas as pd

from modules.keyword_extractor.keyword_extractor_base import KeywordExtractionStrategy
from modules.keyword_extractor.keyword_extractor_default import DefaultKeywordMatcher
from modules.analyzer.ml_roles import AnalyzerRole
from modules.scanner.project_scanner import ProjectScanner
from modules.utils.logger import get_logger

logger = get_logger(__name__)


class MLAnalyzer(ABC):
    """Base class for all machine learning analyzers."""

    def __init__(
            self,
            output_folder,
            role: AnalyzerRole,
            scanner: ProjectScanner,
            keyword_strategy: KeywordExtractionStrategy = None
    ):
        """Initialize MLAnalyzer with role, output path, scanner and keyword strategy."""
        self.output_folder = output_folder
        self.role = role
        self.role_str = str(self.role.value)
        self.scanner = scanner
        self.keyword_strategy = keyword_strategy or DefaultKeywordMatcher()
        self.init_analysis_folder()

    def init_analysis_folder(self):
        """Create analysis folder and backup previous results if needed."""
        consumer_analysis_path = os.path.join(self.output_folder, "analysis")
        os.makedirs(consumer_analysis_path, exist_ok=True)

        results_file = os.path.join(self.output_folder, 'results.csv')
        if not os.path.exists(results_file):
            df = pd.DataFrame(columns=self.dataframe_columns)
            df.to_csv(results_file, index=False)
        else:
            df = pd.read_csv(results_file)
            backup_name = f'results_backup_{int(time.time())}.csv'
            backup_path = os.path.join(self.output_folder, backup_name)
            df.to_csv(backup_path, index=False)

    def analyze_single_file(self, file, repo, *args, **kwargs):
        """Analyze a single file and extract ML-related libraries and keywords."""
        libraries, keywords, list_load_keywords = [], [], []
        if file:
            libraries, keywords, list_load_keywords = self.check_methods(file, *args, **kwargs)
            if keywords:
                logger.info(
                    "Found %s with ML libraries %s and training instruction %s in %s",
                    file, libraries, keywords, repo
                )
        return libraries, keywords, list_load_keywords

    def analyze_project(self, repo_contents, project, directory, *args, **kwargs):
        """Analyze a single project and return a DataFrame with results."""
        df = pd.DataFrame(columns=self.dataframe_columns)
        collected_files = self.scanner.scan(repo_contents)

        for file_path in collected_files:
            _, keywords, _ = self.analyze_single_file(
                file_path, repo_contents, *args, **kwargs
            )
            if keywords:
                for keyword in keywords:
                    row = pd.DataFrame({
                        'ProjectName': f'{project}/{directory}',
                        f'Is ML {self.role_str}': 'Yes',
                        'libraries': keyword['library'],
                        'where': file_path,
                        'keyword': keyword['keyword'],
                        'line_number': keyword['line_number']
                    }, index=[0])
                    df = pd.concat([df, row], ignore_index=True)

        output_file = os.path.join(
            self.output_folder, f'{project}_{directory}_ml_{self.role_str}.csv'
        )
        if not df.empty:
            df.to_csv(output_file, index=False)
        return df

    def analyze_projects_set(self, input_folder, *args, **kwargs):
        """Analyze all projects in a folder and update the results file."""
        results_file = os.path.join(self.output_folder, 'results.csv')
        df = pd.read_csv(results_file)

        for project in os.listdir(input_folder):
            project_path = os.path.join(input_folder, project)
            if not os.path.isdir(project_path):
                continue

            for dir_path in os.listdir(project_path):
                full_dir_path = os.path.join(project_path, dir_path)
                if os.path.isdir(full_dir_path):
                    logger.info("Project: %s", project)
                    new_df = self.analyze_project(
                        full_dir_path,
                        project,
                        dir_path,
                        *args, **kwargs
                    )
                    df = pd.concat([df, new_df], ignore_index=True)
                    df.to_csv(results_file, index=False)

        return df

    @abstractmethod
    def check_methods(self, *args, **kwargs):
        """Abstract method to be implemented for extracting ML-specific features."""
        raise NotImplementedError("Subclasses must implement check_methods")

    @property
    def dataframe_columns(self):
        """Return the default column headers for the result DataFrame."""
        return [
            'ProjectName',
            f'Is ML {self.role_str}',
            'libraries',
            "where",
            "keyword",
            'line_number'
        ]
