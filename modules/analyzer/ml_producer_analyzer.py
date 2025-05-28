import os
import re
import time

import pandas as pd

from modules.analyzer.ml_analyzer import MLAnalyzer

class MLProducerAnalyzer(MLAnalyzer):

    @property
    def dataframe_columns(self):
        return ['ProjectName', 'Is ML producer', 'libraries', 'where', 'keyword', 'line_number']

    def check_training_method(self, file, producer_dict_path):
        producer_library_dict = self.load_library_dict(producer_dict_path)
        producer_related_dict = self.check_ml_library_usage(file, producer_library_dict)
        producer_keywords = producer_related_dict['Keyword'].tolist()
        producer_library_dict_list = producer_related_dict['library'].tolist()

        list_keywords = []
        list_load_keywords = []

        flag = False
        if len(producer_library_dict_list) != 0:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    line_number = 0
                    for line in f:
                        line_number += 1
                        line.replace("(", "\(")
                        for keyword in producer_keywords:
                            # Build regex to handle spaces within keywords
                            if '.' in str(keyword):
                                keyword = keyword.replace('.', '\.')
                            if '\s' in str(keyword):
                                parts = keyword.split()
                                regex = r'\s*'.join(parts)  # Allows optional spaces between parts of the keyword
                                pattern = re.compile(regex, re.IGNORECASE)
                            else:
                                if '(' in str(keyword):
                                    keyword = keyword.replace('(', '\(')
                                pattern = re.compile(str(keyword), re.IGNORECASE)

                            if re.search(pattern, line):
                                flag = True
                                keyword = keyword.replace("\\", "")

                                related_match = producer_related_dict[producer_related_dict['Keyword'] == keyword]

                                found_result = {
                                    'keyword': keyword,
                                    'library': related_match['library'].values[0],
                                    'file': file,
                                    'line': line.strip(),
                                    'line_number': line_number
                                }
                                list_keywords.append(found_result)
                            if flag:
                                flag = False  # Reset flag for next iteration
            except UnicodeDecodeError:
                print(f"Error reading file {file}")
                return producer_library_dict_list, list_keywords, list_load_keywords
            except FileNotFoundError:
                print(f"Error finding file {file}")
                return producer_library_dict_list, list_keywords, list_load_keywords

        return producer_library_dict_list, list_keywords, list_load_keywords

    def analyze_single_file(self, file, repo, library_dict_path):
        keywords = []
        list_load_keywords = []
        libraries = []
        if file:
            libraries, keywords, list_load_keywords = self.check_training_method(file, library_dict_path)
            if len(keywords) > 0:
                print(f"Found {file} with ML libraries{libraries} and training instruction {keywords} in {repo}")
                return libraries, keywords, file
            return libraries, keywords, file
        return libraries, keywords, file


    def analyze_project(self, repo_contents, project, directory, library_dict_path):
        df = pd.DataFrame(columns=self.dataframe_columns)
        for root, dirs, files in os.walk(repo_contents):
            for file in files:
                if file.endswith(('.py', '.ipynb')):
                    file_path = os.path.join(root, file)
                    libraries, keywords, file_path = self.analyze_single_file(file_path, repo_contents, library_dict_path)
                    if keywords:
                        for keyword in keywords:
                            df = pd.concat([
                                df,
                                pd.DataFrame({
                                    'ProjectName': f'{project}/{directory}',
                                    'Is ML producer': 'Yes',
                                    'libraries': keyword['library'],
                                    'where': file_path,
                                    'keyword': keyword['keyword'],
                                    'line_number': keyword['line_number']
                                }, index=[0])
                            ], ignore_index=True)
        output_file = os.path.join(self.output_folder, f'{project}_{directory}_ml_producer.csv')
        if not df.empty:
            df.to_csv(output_file, index=False)
        return df

    def analyze_projects_set(self, input_folder, library_dict_path):
        results_file = os.path.join(self.output_folder, 'results.csv')
        df = pd.read_csv(results_file)

        for project in os.listdir(input_folder):
            if not os.path.isdir(os.path.join(input_folder, project)):
                continue

            for dir in os.listdir(os.path.join(input_folder, project)):
                print("Project:", project)
                if os.path.isdir(os.path.join(input_folder, project, dir)):
                    if not self.baseline_check(project, dir, df):
                        new_df = self.analyze_project(
                            os.path.join(input_folder, project, dir),
                            project,
                            dir,
                            library_dict_path
                        )
                        df = pd.concat([df, new_df], ignore_index=True)
                        df.to_csv(results_file, index=False)

        return df