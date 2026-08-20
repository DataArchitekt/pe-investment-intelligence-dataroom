"""Provider-neutral contracts for future document intelligence integrations."""

from abc import ABC, abstractmethod
from pathlib import Path


class StorageService(ABC):
    @abstractmethod
    def store(self, source: Path, destination: str) -> str: ...


class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, source: Path) -> str: ...


class EmbeddingService(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...


class LLMService(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str: ...


class VectorSearchService(ABC):
    @abstractmethod
    def search(self, deal_id: str, query: str) -> list[dict]: ...
