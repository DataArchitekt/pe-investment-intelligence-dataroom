import re
from pathlib import Path

from app.core.config import PROJECT_ROOT, settings
from app.integrations.contracts import StorageService


class LocalStorageService(StorageService):
    """Filesystem storage for the local MVP; replaceable by an Azure adapter later."""

    def __init__(self, root: Path | None = None) -> None:
        configured_path = Path(settings.document_storage_path)
        self.root = (root or (PROJECT_ROOT / configured_path if not configured_path.is_absolute() else configured_path)).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def save_file(self, deal_id: str, category: str, file_name: str, content: bytes) -> str:
        safe_deal = self._safe_component(deal_id)
        safe_category = self._safe_component(category)
        safe_name = self._safe_filename(file_name)
        directory = self.root / safe_deal / safe_category
        directory.mkdir(parents=True, exist_ok=True)
        destination = self._unique_path(directory, safe_name)
        destination.write_bytes(content)
        return destination.relative_to(self.root).as_posix()

    def get_file(self, file_path: str) -> Path:
        candidate = (self.root / file_path).resolve()
        if self.root not in candidate.parents or not candidate.is_file():
            raise FileNotFoundError("Stored document file was not found")
        return candidate

    def delete_file(self, file_path: str) -> None:
        try:
            self.get_file(file_path).unlink()
        except FileNotFoundError:
            pass

    def file_exists(self, file_path: str) -> bool:
        try:
            self.get_file(file_path)
        except FileNotFoundError:
            return False
        return True

    @staticmethod
    def _safe_component(value: str) -> str:
        return re.sub(r"[^A-Za-z0-9._-]", "_", value).strip("._") or "Other"

    @classmethod
    def _safe_filename(cls, file_name: str) -> str:
        name = Path(file_name).name
        stem = cls._safe_component(Path(name).stem)[:180]
        suffix = re.sub(r"[^A-Za-z0-9.]", "", Path(name).suffix.lower())[:12]
        return f"{stem}{suffix}" if suffix else stem

    @staticmethod
    def _unique_path(directory: Path, file_name: str) -> Path:
        candidate = directory / file_name
        index = 1
        while candidate.exists():
            candidate = directory / f"{Path(file_name).stem} ({index}){Path(file_name).suffix}"
            index += 1
        return candidate
