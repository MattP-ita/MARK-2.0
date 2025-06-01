from modules.analyzer.library_dict_type import LibraryDictType
from modules.analyzer.ml_analyzer_manager import MLAnalyzerManager
from modules.analyzer.ml_consumer_analyzer import MLConsumerAnalyzer
from modules.analyzer.ml_producer_analyzer import MLProducerAnalyzer
from modules.analyzer.ml_roles import AnalyzerRole

MLAnalyzerManager.register_specialization(
    role_name=AnalyzerRole.PRODUCER,
    analyzer_class=MLProducerAnalyzer,
    dict_types=[LibraryDictType.PRODUCER]
)

MLAnalyzerManager.register_specialization(
    role_name=AnalyzerRole.CONSUMER,
    analyzer_class=MLConsumerAnalyzer,
    dict_types=[LibraryDictType.CONSUMER, LibraryDictType.PRODUCER]
)
