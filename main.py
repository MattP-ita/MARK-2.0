from pathlib import Path

from modules.analyzer.analyzer_factory import AnalyzerFactory
from modules.analyzer.builder.consumer_analyzer_builder import ConsumerAnalyzerBuilder
from modules.analyzer.builder.producer_analyzer_builder import ProducerAnalyzerBuilder
from modules.analyzer.ml_analysis_facade import MLAnalysisFacade
from modules.library_manager.library_dict_manager import LibraryDictManager
from modules.library_manager.library_dict_type import LibraryDictType
from modules.analyzer.ml_analyzer_manager import MLAnalyzerManager
from modules.analyzer.ml_roles import AnalyzerRole
from modules.cloner.cloner import RepoCloner
from modules.cloner.cloning_check import RepoInspector
from oracle.matching.results_analysis import ResultAnalysis
from oracle.merge import Merger
from modules.utils.logger import get_logger
logger = get_logger(__name__)


io_path = Path("./io")
output_path=Path("./io/output")
project_list_path=Path("./io/applied_projects.csv")
repository_path=Path("./io/repos")
analyzer_path=Path("./modules/analyzer")
oracle_path=  Path("./oracle")
n_repos=30

def update_library_dict(dict_type: LibraryDictType):
    manager = LibraryDictManager(analyzer_path=analyzer_path)
    added = manager.update_dictionary(
        dict_type=dict_type,
        new_entries_path="new_libs_to_add.csv"
    )
    logger.info(f"Aggiunti {added} nuovi record.")


def main():

    """
    logger.info("*** AGGIORNO LA LIBRARY_DICT ***")
    update_library_dict(LibraryDictType.CONSUMER)
    """

    logger.info("*** CLONER ***")
    cloner = RepoCloner(input_path=project_list_path, output_path=repository_path, n_repos=n_repos)
    cloner.clone_all()

    logger.info("*** CLONER_CHECK ***")
    inspector = RepoInspector(csv_input_path=project_list_path, output_path=repository_path)
    inspector.run_analysis()

    logger.info("*** INIZIO L'ANALISI ***")
    producer_facade = MLAnalysisFacade(input_path=repository_path, io_path=io_path, role=AnalyzerRole.PRODUCER)
    dir_producer = producer_facade.run_analysis()
    consumer_facade = MLAnalysisFacade(input_path=repository_path, io_path=io_path, role=AnalyzerRole.CONSUMER)
    dir_consumer = consumer_facade.run_analysis(rules_3=True)


    logger.info("*** INIZIO IL MERGE ***")

    producer_merger = Merger(column_name="producer", oracle_path=oracle_path)
    producer_merger.reporting(base_output_path=output_path, dir_result=dir_producer, file_name="results.csv")

    consumer_merger = Merger(column_name="consumer", oracle_path=oracle_path)
    consumer_merger.reporting(base_output_path=output_path, dir_result=dir_consumer, file_name="results.csv")

    """
    logger.info("*** INIZIO LA RESULT ANALYSIS ***")
    producer_analysis = ResultAnalysis(column_name="producer", oracle_path=oracle_path, folder_path=output_path, dir_result= dir_producer, file_name=dir_producer)
    consumer_analysis = ResultAnalysis(column_name="consumer", oracle_path=oracle_path, folder_path=output_path, dir_result= dir_consumer, file_name=dir_consumer)
    producer_analysis.start_analysis()
    consumer_analysis.start_analysis()
     """


if __name__ == "__main__":
    main()
