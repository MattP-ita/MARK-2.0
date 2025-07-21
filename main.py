"""Main script to orchestrate the ML analysis pipeline."""

from pathlib import Path
from modules.analyzer.ml_analysis_facade import MLAnalysisFacade
from modules.analyzer.ml_roles import AnalyzerRole
from modules.cloner.cloner import RepoCloner
from modules.cloner.cloning_check import RepoInspector
from modules.library_manager.library_dict_manager import LibraryDictManager
from modules.library_manager.library_dict_type import LibraryDictType
from modules.utils.logger import get_logger
from oracle.matching.results_analysis import ResultAnalysis
from oracle.merge import Merger
from modules.analyzer.analyzer_factory import AnalyzerFactory  # required import
from modules.analyzer.builder.consumer_analyzer_builder import (
    ConsumerAnalyzerBuilder
) # required import
from modules.analyzer.builder.producer_analyzer_builder import (
    ProducerAnalyzerBuilder
) # required import

logger = get_logger(__name__)

# Define global paths and constants
IO_PATH = Path("./io")
OUTPUT_PATH = IO_PATH / "output"
PROJECT_LIST_PATH = IO_PATH / "applied_projects.csv"
REPOSITORY_PATH = IO_PATH / "repos"
ANALYZER_PATH = Path("./modules/analyzer")
ORACLE_PATH = Path("./oracle")
N_REPOS = 100


def update_library_dict(dict_type: LibraryDictType) -> None:
    """Update the library dictionary with new entries."""
    manager = LibraryDictManager(analyzer_path=ANALYZER_PATH)
    added = manager.update_dictionary(
        dict_type=dict_type,
        new_entries_path="new_libs_to_add.csv"
    )
    logger.info("Aggiunti %d nuovi record.", added)


def main() -> None:
    """
    # === AGGIORNAMENTO LIBRARY DICTIONARY ===
    logger.info("*** AGGIORNO LA LIBRARY_DICT ***")
    update_library_dict(LibraryDictType.CONSUMER)
    """
    # === CLONAZIONE DEI REPOSITORY ===
    logger.info("*** CLONER ***")
    cloner = RepoCloner(
        input_path=PROJECT_LIST_PATH,
        output_path=REPOSITORY_PATH,
        n_repos=N_REPOS
    )
    cloner.clone_all()

    # === VERIFICA CLONAZIONE ===
    logger.info("*** CLONER_CHECK ***")
    inspector = RepoInspector(
        csv_input_path=PROJECT_LIST_PATH,
        output_path=REPOSITORY_PATH
    )
    inspector.run_analysis()

    # === ANALISI ML ===
    logger.info("*** INIZIO L'ANALISI ***")
    producer_facade = MLAnalysisFacade(
        input_path=REPOSITORY_PATH,
        io_path=IO_PATH,
        role=AnalyzerRole.PRODUCER
    )
    dir_producer = producer_facade.run_analysis()

    consumer_facade = MLAnalysisFacade(
        input_path=REPOSITORY_PATH,
        io_path=IO_PATH,
        role=AnalyzerRole.CONSUMER
    )
    dir_consumer = consumer_facade.run_analysis(rules_3=True)

    # === MERGE DEI RISULTATI ===
    logger.info("*** INIZIO IL MERGE ***")
    producer_merger = Merger(
        column_name="producer",
        oracle_path=ORACLE_PATH
    )
    producer_merger.reporting(
        base_output_path=OUTPUT_PATH,
        dir_result=dir_producer,
        file_name="results.csv"
    )

    consumer_merger = Merger(
        column_name="consumer",
        oracle_path=ORACLE_PATH
    )
    consumer_merger.reporting(
        base_output_path=OUTPUT_PATH,
        dir_result=dir_consumer,
        file_name="results.csv"
    )

    # === ANALISI FINALE DEI RISULTATI ===
    logger.info("*** INIZIO LA RESULT ANALYSIS ***")
    producer_analysis = ResultAnalysis(
        role=AnalyzerRole.PRODUCER,
        oracle_path=ORACLE_PATH,
        base_folder_path=OUTPUT_PATH,
        results_subdir=dir_producer
    )
    consumer_analysis = ResultAnalysis(
        role=AnalyzerRole.CONSUMER,
        oracle_path=ORACLE_PATH,
        base_folder_path=OUTPUT_PATH,
        results_subdir=dir_consumer
    )

    producer_analysis.start_analysis()
    consumer_analysis.start_analysis()


if __name__ == "__main__":
    main()
