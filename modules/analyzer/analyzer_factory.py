from typing import Callable

from modules.analyzer.builder.analyzer_builder import AnalyzerBuilder
from modules.analyzer.ml_roles import AnalyzerRole
from modules.utils.logger import get_logger
logger = get_logger(__name__)

class AnalyzerFactory:
    _registry = {}

    @classmethod
    def register(cls, role: AnalyzerRole):
        logger.info('New builder for role %s', role)
        def inner_wrapper(wrapped_class: AnalyzerBuilder) -> AnalyzerBuilder:
            if role in cls._registry:
                logger.warning('A builder for role %s already exists. Will replace it', role)

            cls._registry[role] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def create_builder(cls, role: AnalyzerRole) -> AnalyzerBuilder:
        if role not in cls._registry:
            raise ValueError(f"Builder for role '{role}' not registered.")

        return cls._registry[role]()
