"""Module to analyze ML role classification results against an oracle."""

import os
import pandas as pd
from modules.analyzer.ml_roles import AnalyzerRole


class ResultAnalysis:
    """Performs comparison between detected ML roles and oracle values."""

    def __init__(
        self,
        role: AnalyzerRole,
        oracle_path: str,
        base_folder_path: str,
        results_subdir: str
    ):
        """
        Initialize ResultAnalysis.

        Args:
            role (AnalyzerRole): Role to evaluate (PRODUCER or CONSUMER).
            oracle_path (str): Path to the oracle files.
            base_folder_path (str): Root path containing result subdirectories.
            results_subdir (str): Subdirectory within the role folder.
            file_name (str): Output file name (without full path).
        """
        self.role = role
        self.role_str = str(role.value)
        self.oracle_path = oracle_path
        self.folder_path = os.path.join(base_folder_path, self.role_str, results_subdir)
        self.file_name = results_subdir

    def start_analysis(self):
        """Compare predictions with oracle and export result to CSV."""
        oracle_file = os.path.join(self.oracle_path, f"oracle_{self.role_str}.csv")
        if not os.path.exists(oracle_file):
            raise FileNotFoundError(f"Oracle file not found: {oracle_file}")
        if not os.path.isdir(self.folder_path):
            raise FileNotFoundError(f"Results folder not found: {self.folder_path}")

        oracle_df = pd.read_csv(oracle_file)
        result_df = oracle_df[["ProjectName", f"Is_Real_ML_{self.role_str}"]].copy()
        result_df[f"is ML {self.role_str}"] = "No"

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(self.folder_path, filename)
                df = pd.read_csv(file_path)
                matching = result_df["ProjectName"].isin(df["ProjectName"])
                result_df.loc[matching, f"is ML {self.role_str}"] = "Yes"

        output_dir = os.path.join(self.oracle_path, "matching")
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, f"result_{self.file_name}.csv")
        result_df.to_csv(output_file, index=False)
