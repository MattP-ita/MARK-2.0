from modules.analyzer.ml_roles import AnalyzerRole


class AnalyzerFactory:
    _registry = {}

    @classmethod
    def register(cls, role: AnalyzerRole, builder_cls):
        cls._registry[role] = builder_cls

    @classmethod
    def from_role(cls, role: AnalyzerRole):
        if role not in cls._registry:
            raise ValueError(f"Builder for role '{role}' not registered.")
        return cls._registry[role]()
