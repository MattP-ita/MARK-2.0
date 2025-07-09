import os
import git
from pathlib import Path
import pandas as pd
from git import Repo
import concurrent.futures
from threading import Lock

from modules.utils.logger import get_logger
logger = get_logger(__name__)


class RepoCloner:
    def __init__(self, input_path, output_path, n_repos=5, log_dir=Path("./modules/cloner/log")):
        self.input_path = input_path
        self.output_path = output_path
        self.n_repos = n_repos
        self.writer_lock = Lock()
        self.cloned_log_path = os.path.join(log_dir, 'cloned_log.csv')
        self.error_log_path = os.path.join(log_dir, 'errors.csv')

    def _clone_repo(self, row):
        repo_full_name = row["ProjectName"]
        repo_url = f'https://github.com/{repo_full_name}.git'
        dest_path = os.path.join(self.output_path, repo_full_name)

        try:
            logger.info(f'Cloning {repo_full_name}')
            Repo.clone_from(repo_url, str(dest_path), depth=1)
            logger.info(f'Cloned {repo_full_name}')
        except git.exc.GitError as e:
            logger.error(f'Error cloning {repo_full_name}')
            with self.writer_lock:
                with open(self.error_log_path, 'a', encoding='utf-8') as error_log:
                    error = str(e).replace("'", "").replace("\n", "")
                    error_log.write(f"{repo_full_name},{repo_url},'{error}'\n")
            return

        with self.writer_lock:
            try:
                cloned_log = pd.read_csv(self.cloned_log_path)
                cloned_log = pd.concat([cloned_log, pd.DataFrame([row])], ignore_index=True)
                cloned_log.to_csv(self.cloned_log_path, index=False)
            except Exception as e:
                logger.error(f'Error saving log for {repo_full_name}: {e}')

    def load_repos_to_clone(self):
        df = pd.read_csv(self.input_path, delimiter=",")
        df = df.head(self.n_repos) 

        if os.path.exists(self.cloned_log_path):
            cloned_log = pd.read_csv(self.cloned_log_path)
            df = df[~df['ProjectName'].isin(cloned_log['ProjectName'])]
        else:
            pd.DataFrame(columns=['ProjectName', 'repo_url', 'ml_libs', 'count']).to_csv(self.cloned_log_path,
                                                                                         index=False)
        return df

    def clone_all(self, max_workers=None):
        df = self.load_repos_to_clone()
        logger.info(f'To analyze: {len(df)} repositories')

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._clone_repo, row) for _, row in df.iterrows()]
            for future in concurrent.futures.as_completed(futures):
                pass  
