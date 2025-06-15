from modules.analyzer.analyzer_factory import AnalyzerFactory

def register_builder(role):
    def decorator(cls):
        AnalyzerFactory.register(role, cls)
        return cls
    return decorator
