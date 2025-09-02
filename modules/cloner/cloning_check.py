"""Utility to verify which GitHub repositories were successfully cloned.

This module reads the list of projects from an input CSV, inspects the output
directory on disk, and produces two reports:
- not_cloned_repos.csv : projects listed in the CSV but not found on disk
- effective_repos.csv  : complete list of repositories actually detected on disk
"""

import os
from pathlib import Path
import pandas as pd

from modules.utils.logger import get_logger
logger = get_logger(__name__)


class RepoInspector:
    """Class to analyze the results of the cloning process of GitHub repositories."""

    def __init__(self, csv_input_path, output_path, log_dir=Path("./modules/cloner/log")):
        """Initialize RepoInspector with paths to input CSV, output folder and log directory."""
        self.csv_input_path = csv_input_path
        self.output_path = output_path
        self.not_cloned_repos = os.path.join(log_dir, 'not_cloned_repos.csv')
        self.effective_repos = os.path.join(log_dir, 'effective_repos.csv')

    # ---------------------------------------------------------------------
    # Filesystem checks
    # ---------------------------------------------------------------------

    def check_cloned_repo(self, project_name):
        """Check if the repository directory exists and is not empty."""
        repo_base_path = os.path.join(self.output_path, project_name.split('/')[0])
        if os.path.exists(repo_base_path):
            return len(os.listdir(str(repo_base_path))) > 0
        return False

    # ---------------------------------------------------------------------
    # DataFrame selections
    # ---------------------------------------------------------------------

    def get_not_cloned_list(self, df):
        """Return list of repositories from the input CSV that were not cloned."""
        return [row for _, row in df.iterrows() if not self.check_cloned_repo(row['ProjectName'])]

    def get_cloned_list(self, df):
        """Return list of repositories from the input CSV that were cloned."""
        return [row for _, row in df.iterrows() if self.check_cloned_repo(row['ProjectName'])]

    # ---------------------------------------------------------------------
    # Aggregated detections
    # ---------------------------------------------------------------------

    def count_effective_repos(self):
        """Count total number of cloned repositories across all directories."""
        count = 0
        for dir_name in os.listdir(self.output_path):
            full_dir = os.path.join(self.output_path, dir_name)
            if os.path.isdir(full_dir):
                count += len(os.listdir(full_dir))
        return count

    def get_effective_repos(self):
        """Return a DataFrame with all detected cloned repositories and their paths."""
        repos = pd.DataFrame(columns=['ProjectName', 'repo_path'])
        for dir_name in os.listdir(self.output_path):
            dir_path = os.path.join(self.output_path, dir_name)
            if not os.path.isdir(dir_path):
                continue
            for repo in os.listdir(dir_path):
                repo_path = os.path.join(dir_path, repo)
                project_name = f"{dir_name}/{repo}"
                repos = pd.concat([repos, pd.DataFrame({
                    'ProjectName': [project_name],
                    'repo_path': [repo_path]
                })], ignore_index=True)
        return repos

    # ---------------------------------------------------------------------
    # Orchestration
    # ---------------------------------------------------------------------

    def run_analysis(self):
        """Run the full inspection: log cloned, not cloned, and effective repos to CSV."""
        if os.path.exists(self.not_cloned_repos):
            os.remove(self.not_cloned_repos)

        df = pd.read_csv(self.csv_input_path)
        not_cloned = self.get_not_cloned_list(df)
        cloned = self.get_cloned_list(df)

        logger.info('cloned: %d repos', len(cloned))
        logger.info('not cloned: %d repos', len(not_cloned))

        pd.DataFrame(not_cloned).to_csv(self.not_cloned_repos, index=False)

        effective_count = self.count_effective_repos()
        logger.info('effective repos: %d', effective_count)

        effective_repos = self.get_effective_repos()
        effective_repos.to_csv(self.effective_repos, index=False)
