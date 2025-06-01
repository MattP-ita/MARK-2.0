import modules.analyzer.analyzer_registry
from pathlib import Path

from modules.analyzer.exec_analysis import analyze_producers, analyze_consumers
from modules.analyzer.library_dict_manager import LibraryDictManager
from modules.analyzer.library_dict_type import LibraryDictType
from modules.analyzer.ml_analyzer_manager import MLAnalyzerManager
from modules.analyzer.ml_consumer_analyzer import MLConsumerAnalyzer
from modules.analyzer.ml_producer_analyzer import MLProducerAnalyzer
from modules.analyzer.ml_roles import AnalyzerRole
from modules.cloner.cloner import RepoCloner
from modules.cloner.cloning_check import RepoInspector
from oracle.matching.results_analysis import ResultAnalysis
from oracle.merge import Merger

project_list_path=Path("./modules/cloner/applied_projects.csv")
repository_path=Path("./repos")
analyzer_path=Path("./modules/analyzer")
output_path=Path("./modules/analyzer/output")
oracle_path=  Path("./oracle")
n_repos=40

def update_library_dict(dict_type: LibraryDictType):
    manager = LibraryDictManager(analyzer_path=analyzer_path)
    added = manager.update_dictionary(
        dict_type=dict_type,
        new_entries_path="new_libs_to_add.csv"
    )
    print(f"Aggiunti {added} nuovi record.")


def main():
    """
    print("*** AGGIORNO LA LIBRARY_DICT ***")
    update_library_dict(LibraryDictType.CONSUMER)
    """
    """  
    print("*** CLONER ***")
    cloner = RepoCloner(input_path=project_list_path, output_path=repository_path, n_repos=n_repos)
    cloner.clone_all()

    print("*** CLONER_CHECK ***")
    inspector = RepoInspector(csv_input_path=project_list_path, output_path=repository_path)
    inspector.run_analysis()

    print("*** INIZIO L'ANALISI ***")
    producer_manager = MLAnalyzerManager.from_role(AnalyzerRole.PRODUCER)
    dir_producer = producer_manager.analyze(input_path=repository_path, output_path=output_path, analyzer_path=analyzer_path)

    consumer_manager = MLAnalyzerManager.from_role(AnalyzerRole.CONSUMER)
    dir_consumer = consumer_manager.analyze(input_path=repository_path, output_path=output_path, analyzer_path=analyzer_path, rules_3=True, rules_4=True)
    """
    """   
    dir_producer = analyze_producers(input_path=repository_path, output_path=output_path)
    dir_consumer = analyze_consumers(input_path=repository_path, output_path=output_path)
    """
    """   
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
    """

if __name__ == "__main__":
    main()
