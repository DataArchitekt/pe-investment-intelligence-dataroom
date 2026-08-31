"""Provider-neutral contracts for future document intelligence integrations."""

from abc import ABC, abstractmethod
from pathlib import Path


class StorageService(ABC):
    @abstractmethod
    def save_file(self, deal_id: str, category: str, file_name: str, content: bytes) -> str: ...

    @abstractmethod
    def get_file(self, file_path: str) -> Path: ...

    @abstractmethod
    def delete_file(self, file_path: str) -> None: ...

    @abstractmethod
    def file_exists(self, file_path: str) -> bool: ...


class DocumentProcessor(ABC):
    @abstractmethod
    def extract(self, source: Path) -> list[object]: ...


class EmbeddingService(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...


class LLMService(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str: ...


class VectorSearchService(ABC):
    @abstractmethod
    def search(self, deal_id: str, query: str) -> list[dict]: ...
