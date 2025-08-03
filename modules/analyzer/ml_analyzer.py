"""Abstract base class for ML analyzers handling project scans and keyword detection."""

import os
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

    def analyze_single_file(self, file, repo, *args, **kwargs):
        """Analyze a single file and extract ML-related libraries and keywords."""
        if not os.path.isfile(file):
            return [], [], []

        libraries, keywords, list_load_keywords = self.check_library(file, *args, **kwargs)
        if keywords:
            logger.info(""
                "Found %s with ML libraries %s and training instruction %s in %s",
                file, libraries, keywords, repo
            )
        return libraries, keywords, list_load_keywords

    def analyze_project(self, repo, project, directory, *args, **kwargs):
        """Analyze a single project and return a DataFrame with results."""
        rows = []
        for root, _, files in os.walk(repo):
            for filename in files:
                if not self.scanner.is_valid_file(filename):
                    continue

                file_path = os.path.join(root, filename)
                _, keywords, _ = self.analyze_single_file(
                    file_path, repo, *args, **kwargs
                )
                if keywords:
                    for keyword in keywords:
                        rows.append({
                            'ProjectName': f'{project}/{directory}',
                            f'Is ML {self.role_str}': 'Yes',
                            'libraries': keyword['library'],
                            'where': file_path,
                            'keyword': keyword['keyword'],
                            'line_number': keyword['line_number']
                        })

        df = pd.DataFrame(rows)
        if not df.empty:
            output_file = os.path.join(
                self.output_folder, f'{project}_{directory}_ml_{self.role_str}.csv'
            )
            df.to_csv(output_file, index=False)

        return df

    def analyze_projects_set(self, input_folder, *args, **kwargs):
        """Analyze all projects in a folder and update the results file."""
        all_rows = []
        for project in os.listdir(input_folder):
            project_path = os.path.join(input_folder, project)
            if not os.path.isdir(project_path):
                continue

            for dir_path in os.listdir(project_path):
                full_dir_path = os.path.join(project_path, dir_path)
                if not os.path.isdir(full_dir_path):
                    continue

                logger.info("Project: %s", project)
                df = self.analyze_project(
                    full_dir_path,
                    project,
                    dir_path,
                    *args, **kwargs)
                if not df.empty:
                    all_rows.extend(df.to_dict(orient='records'))

        final_df = pd.DataFrame(all_rows)
        if not final_df.empty:
            results_file = os.path.join(self.output_folder, 'results.csv')
            final_df.to_csv(results_file, index=False)

        return final_df


    @abstractmethod
    def check_library(self, *args, **kwargs):
        """Abstract method to be implemented for extracting ML-specific features."""
        raise NotImplementedError("Subclasses must implement check_library")
