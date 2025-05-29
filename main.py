from pathlib import Path

from modules.analyzer.exec_analysis import analyze_producers, analyze_consumers
from modules.cloner.cloner import RepoCloner
from modules.cloner.cloning_check import RepoInspector
from oracle.matching.results_analysis import ResultAnalysis
from oracle.merge import Merger


def main():
    project_list_path=Path("./modules/cloner/applied_projects.csv")
    repository_path=Path("./repos")
    analyzer_path=Path("./modules/analyzer")
    output_path=Path("./modules/analyzer/output")
    oracle_path=  Path("./oracle")
    n_repos=40

    print("*** CLONER ***")
    cloner = RepoCloner(input_path=project_list_path, output_path=repository_path, n_repos=n_repos)
    cloner.clone_all()

    print("*** CLONER_CHECK ***")
    inspector = RepoInspector(csv_input_path=project_list_path, output_path=repository_path)
    inspector.run_analysis()

    print("*** INIZIO L'ANALISI ***")
    dir_producer = analyze_producers(input_path=repository_path, output_path=output_path)
    dir_consumer = analyze_consumers(input_path=repository_path, output_path=output_path)


    print("*** INIZIO IL MERGE ***")
    producer_merger = Merger(column_name="producer", oracle_path=oracle_path)
    consumer_merger = Merger(column_name="consumer", oracle_path=oracle_path)
    producer_merger.reporting(base_output_path=output_path, dir_result=dir_producer, file_name="results.csv")
    consumer_merger.reporting(base_output_path=output_path, dir_result=dir_consumer, file_name="results.csv")

    print("*** INIZIO LA RESULT ANALYSIS ***")
    producer_analysis = ResultAnalysis(column_name="producer", oracle_path=oracle_path, folder_path=output_path, dir_result= dir_producer, file_name=dir_producer)
    consumer_analysis = ResultAnalysis(column_name="consumer", oracle_path=oracle_path, folder_path=output_path, dir_result= dir_consumer, file_name=dir_consumer)
    producer_analysis.start_analysis()
    consumer_analysis.start_analysis()



if __name__ == "__main__":
    main()
