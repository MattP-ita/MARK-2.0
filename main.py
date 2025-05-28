from pathlib import Path

from modules.analyzer.exec_analysis import analyze_producers, analyze_consumers
from modules.cloner.cloner import RepoCloner
from modules.cloner.cloning_check import RepoInspector

def main():
    project_list_path=Path("./modules/cloner/applied_projects.csv")
    repository_path=Path("./repos")
    analyzer_path=Path("./modules/analyzer")
    output_path=Path("./modules/analyzer/output")
    n_repos=40

    print("*** CLONER ***")
    cloner = RepoCloner(input_path=project_list_path, output_path=repository_path, n_repos=n_repos)
    cloner.clone_all()

    print("*** CLONER_CHECK ***")
    inspector = RepoInspector(csv_input_path=project_list_path, output_path=repository_path)
    inspector.run_analysis()

    print("*** INIZIO L'ANALISI ***")
    analyze_producers(input_path=repository_path, output_path=output_path, analyzer_path=analyzer_path)
    analyze_consumers(input_path=repository_path, output_path=output_path, analyzer_path=analyzer_path)



if __name__ == "__main__":
    main()
