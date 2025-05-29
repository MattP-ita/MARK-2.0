import os
import pandas as pd

class ResultAnalysis:
    def __init__(self, column_name, oracle_path, folder_path, dir_result, file_name):
        self.column_name = column_name
        self.oracle_path = oracle_path
        self.folder_path = str(os.path.join(folder_path, column_name, dir_result))
        self.file_name = file_name

    def start_analysis(self):
        # Load the oracle.csv file
        oracle_df = pd.read_csv(os.path.join(self.oracle_path, f"oracle_{self.column_name}.csv"))

        # Create a new dataframe with the required columns
        result_df = oracle_df[["ProjectName", f"Is_Real_ML_{self.column_name}"]].copy()

        # Add the "is ML Producer" column
        result_df[f"is ML {self.column_name}"] = "No"

        # Check each .csv file in the file_name folder
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".csv"):
                # Read the current CSV file
                file_path = os.path.join(self.folder_path, filename)
                df = pd.read_csv(file_path)

                # Check for matching ProjectName values
                matching_projects = result_df["ProjectName"].isin(df["ProjectName"])
                result_df.loc[matching_projects, f"is ML {self.column_name}"] = "Yes"

        # Save the resulting dataframe to a new CSV file
        result_df.to_csv(os.path.join(self.oracle_path, "matching", f"result_{self.file_name}.csv"), index=False)