from abc import ABC, abstractmethod

class KeywordExtractionStrategy(ABC):
    @abstractmethod
    def extract_keywords(self, file: str, related_dict) -> list[dict]:
        pass
