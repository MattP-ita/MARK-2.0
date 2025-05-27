from pathlib import Path

from modules.cloner.cloner import RepoCloner
from modules.cloner.cloning_check import RepoInspector

def main():
    project_list_path= Path("./modules/cloner/applied_projects.csv")
    repository_path=  Path("./repos")
    n_repos=40

    print("*** CLONER ***")
    cloner = RepoCloner(input_path=project_list_path, output_path=repository_path, n_repos=n_repos)
    cloner.clone_all()

    print("*** CLONER_CHECK ***")
    inspector = RepoInspector(csv_input_path=project_list_path, output_path=repository_path)
    inspector.run_analysis()




if __name__ == "__main__":
    main()
