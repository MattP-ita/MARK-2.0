import os
import pandas as pd


class RepoInspector:
    def __init__(self, csv_input_path, output_path, log_dir="./log"):
        self.csv_input_path = csv_input_path
        self.output_path = output_path
        self.not_cloned_repos = os.path.join(log_dir, 'not_cloned_repos.csv')
        self.effective_repos = os.path.join(log_dir, 'effective_repos.csv')

    def check_cloned_repo(self, project_name):
        repo_base_path = os.path.join(self.output_path, project_name.split('/')[0])
        if os.path.exists(repo_base_path):
            return len(os.listdir(str(repo_base_path))) > 0
        return False

    def get_not_cloned_list(self, df):
        return [row for _, row in df.iterrows() if not self.check_cloned_repo(row['ProjectName'])]

    def get_cloned_list(self, df):
        return [row for _, row in df.iterrows() if self.check_cloned_repo(row['ProjectName'])]

    def count_effective_repos(self):
        count = 0
        for dir_name in os.listdir(self.output_path):
            full_dir = os.path.join(self.output_path, dir_name)
            if os.path.isdir(full_dir):
                count += len(os.listdir(full_dir))
        return count

    def get_effective_repos(self):
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

    def run_analysis(self):

        if os.path.exists(self.not_cloned_repos):
            os.remove(self.not_cloned_repos)

        df = pd.read_csv(self.csv_input_path)
        not_cloned = self.get_not_cloned_list(df)
        cloned = self.get_cloned_list(df)

        print(f'cloned: {len(cloned)} repos')
        print(f'not cloned: {len(not_cloned)} repos')

        pd.DataFrame(not_cloned).to_csv(self.not_cloned_repos, index=False)

        effective_count = self.count_effective_repos()
        print(f'effective repos: {effective_count}')

        effective_repos = self.get_effective_repos()
        effective_repos.to_csv(self.effective_repos, index=False)
