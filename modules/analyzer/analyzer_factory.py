"""Factory for registering and creating analyzer builders based on their roles."""

from modules.analyzer.builder.analyzer_builder import AnalyzerBuilder
from modules.analyzer.ml_roles import AnalyzerRole
from modules.utils.logger import get_logger

logger = get_logger(__name__)


class AnalyzerFactory:
    """Factory class for managing and instantiating AnalyzerBuilder classes by role."""

    _registry = {}

    @classmethod
    def register(cls, role: AnalyzerRole):
        """Decorator to register a builder class for a specific AnalyzerRole.

        If a builder is already registered for the role, it will be replaced.

        Args:
            role (AnalyzerRole): The role for which the builder is being registered.

        Returns:
            Callable[[AnalyzerBuilder], AnalyzerBuilder]: The decorator.
        """
        logger.info("New builder for role %s", role)

        def inner_wrapper(wrapped_class: AnalyzerBuilder) -> AnalyzerBuilder:
            if role in cls._registry:
                logger.warning(
                    "A builder for role %s already exists. Will replace it", role
                )

            cls._registry[role] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def create_builder(cls, role: AnalyzerRole) -> AnalyzerBuilder:
        """Instantiate a registered AnalyzerBuilder based on the provided role.

        Args:
            role (AnalyzerRole): The role for which the builder is requested.

        Returns:
            AnalyzerBuilder: An instance of the registered builder.

        Raises:
            ValueError: If no builder is registered for the given role.
        """
        if role not in cls._registry:
            raise ValueError(f"Builder for role '{role}' not registered.")

        return cls._registry[role]()
