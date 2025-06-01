import os
import re
import time
from abc import ABC

import pandas as pd

from modules.analyzer.library_extractor import LibraryExtractor
from modules.analyzer.ml_analyzer import MLAnalyzer


class MLConsumerAnalyzer(MLAnalyzer):

    @property
    def dataframe_columns(self):
        return ['ProjectName', 'Is ML consumer', 'where', 'keyword', 'line_number', 'libraries']

    def check_training_method(self, file, consumer_dict_path):
        consumer_library_dict = self.load_library_dict(consumer_dict_path)
        consumer_related_dict = self.check_ml_library_usage(file, consumer_library_dict)
        consumer_keywords = consumer_related_dict['Keyword'].tolist()
        consumer_library_dict_list = consumer_related_dict['library'].tolist()

        if len(consumer_library_dict_list) == 0:
            return False
        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
            # check the presence of method that are consumer
            if len(consumer_library_dict_list) != 0:
                for keyword in consumer_keywords:
                    if keyword in file_content:
                        return True
                return False
            return False


    def check_inference_method(self, file, consumer_library, producer_library, rules_3):
        list_keywords = []
        list_load_keywords = []

        # Load the consumer library dictionary dynamically
        consumer_library_dict = self.load_library_dict(consumer_library)
        consumer_related_dict = self.check_ml_library_usage(file, consumer_library_dict)
        consumer_keywords = consumer_related_dict['Keyword'].tolist()
        consumer_library_dict_list = consumer_related_dict['library'].tolist()

        flag = False
        # First, check if the file uses ML libraries
        if len(consumer_library_dict_list) != 0:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    line_number = 0
                    for line in f:
                        line_number += 1
                        for keyword in consumer_keywords:
                            if '.' in str(keyword):
                                keyword = keyword.replace('.', '\.')
                            # Build regex to handle spaces within keywords
                            if '\s' in str(keyword):
                                parts = keyword.split()
                                regex = r'\s*'.join(parts)  # Allows optional spaces between parts of the keyword
                                pattern = re.compile(regex, re.IGNORECASE)
                            else:
                                if '(' in str(keyword):
                                    keyword = keyword.replace('(', '\(')
                                pattern = re.compile(str(keyword), re.IGNORECASE)
                            if re.search(pattern, line):
                                if rules_3:
                                    # here we have to check if the training is performed within the same file
                                    # get library of the keyword
                                    if self.check_training_method(file, producer_library):
                                        flag = False
                                    else:
                                        flag = True
                                else:
                                    flag = True

                            if flag:
                                keyword = keyword.replace("\\", "")

                                related_match = consumer_related_dict[consumer_related_dict['Keyword'] == keyword]

                                found_result = {
                                    'keyword': keyword,
                                    'library': related_match['library'].values[0],
                                    'file': file,
                                    'line': line.strip(),
                                    'line_number': line_number
                                }
                                list_keywords.append(found_result)
                                flag = False  # Reset flag for next iteration
            except UnicodeDecodeError:
                print(f"Error reading file {file}")
                return consumer_library_dict_list, list_keywords, list_load_keywords
            except FileNotFoundError:
                print(f"Error finding file {file}")
                return consumer_library_dict_list, list_keywords, list_load_keywords
        return consumer_library_dict_list, list_keywords, list_load_keywords


    def analyze_single_file(self, file, repo, consumer_library, producer_library, rules_3):
        keywords = []
        list_load_keywords = []
        libraries = []
        if file:
            libraries, keywords, list_load_keywords = self.check_inference_method(file, consumer_library, producer_library, rules_3)
            if len(keywords) > 0:
                print(f"Found {file} with ML libraries{libraries} and training instruction {keywords} in {repo}")
                return libraries, keywords, list_load_keywords, file
            return libraries, keywords, list_load_keywords, file
        return libraries, keywords, list_load_keywords, file


    def analyze_project(self, repo_contents, project, in_dir, consumer_library, producer_library, rules_3, rules_4):
        df = pd.DataFrame(columns=['ProjectName', 'Is ML consumer', 'libraries', "where", "keywords", 'line_number'])
        for root, dirs, files in os.walk(repo_contents):
            for file in files:
                if file.endswith(('.py', '.ipynb')):
                    # added rule 4 conditions for ablations
                    if rules_4 and re.search(r"test|example|eval|validat", file, re.IGNORECASE):
                        continue
                    file_path = os.path.join(root, file)
                    libraries, keywords, list_load_keywords, file_path = self.analyze_single_file(file_path,
                                                                                                  repo_contents,
                                                                                                  consumer_library,
                                                                                                  producer_library,
                                                                                                  rules_3)
                    if keywords:
                        for keyword in keywords:
                            df = pd.concat([
                                df,
                                pd.DataFrame({
                                    'ProjectName': f'{project}/{in_dir}',
                                    'Is ML consumer': 'Yes',
                                    'libraries': keyword['library'],
                                    'where': file_path,
                                    'keywords': keyword['keyword'],
                                    'line_number': keyword['line_number']
                                }, index=[0])
                            ], ignore_index=True)
        output_file = os.path.join(self.output_folder, f'{project}_{in_dir}_ml_consumer.csv')
        if not df.empty:
            df.to_csv(output_file, index=False)
        return df


    def analyze_projects_set(self, input_folder, consumer_library, producer_library, rules_3, rules_4):
        results_file = os.path.join(self.output_folder, 'results.csv')
        df = pd.read_csv(results_file)
        print(f'TEST {consumer_library} - {producer_library}')
        for project in os.listdir(input_folder):
            if not os.path.isdir(os.path.join(input_folder, project)):
                continue

            for dir in os.listdir(os.path.join(input_folder, project)):
                print("Project:", project)
                if os.path.isdir(os.path.join(input_folder, project, dir)):
                    new_df = self.analyze_project(
                        os.path.join(input_folder, project, dir),
                        project,
                        dir,
                        consumer_library, producer_library, rules_3, rules_4
                    )
                    df = pd.concat([df, new_df], ignore_index=True)
                    df.to_csv(results_file, index=False)

        return df