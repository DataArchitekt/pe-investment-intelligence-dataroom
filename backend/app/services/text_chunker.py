import re
from dataclasses import dataclass

from app.core.config import settings


@dataclass(frozen=True)
class ExtractedBlock:
    text: str
    section: str | None = None


@dataclass(frozen=True)
class ExtractedPage:
    page_number: int | None
    blocks: list[ExtractedBlock]


@dataclass(frozen=True)
class ChunkDraft:
    chunk_text: str
    page_number: int | None
    section: str | None
    token_count: int
    char_count: int


def clean_text(value: str) -> str:
    """Conservative cleanup that keeps figures, punctuation, and headings intact."""
    value = value.replace("\x00", "")
    value = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f]", "", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n[ \t]+", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


class TextChunker:
    """Deterministic word-based chunking; words are a documented token approximation."""

    def __init__(self, chunk_size_words: int | None = None, overlap_words: int | None = None) -> None:
        self.chunk_size_words = chunk_size_words or settings.document_chunk_size_words
        self.overlap_words = overlap_words if overlap_words is not None else settings.document_chunk_overlap_words
        if self.chunk_size_words < 1 or self.overlap_words < 0 or self.overlap_words >= self.chunk_size_words:
            raise ValueError("Chunk overlap must be non-negative and smaller than the chunk size")

    def chunk(self, pages: list[ExtractedPage]) -> list[ChunkDraft]:
        drafts: list[ChunkDraft] = []
        for page in pages:
            blocks = [ExtractedBlock(clean_text(block.text), block.section) for block in page.blocks]
            blocks = [block for block in blocks if block.text]
            drafts.extend(self._chunk_page(page.page_number, blocks))
        return drafts

    def _chunk_page(self, page_number: int | None, blocks: list[ExtractedBlock]) -> list[ChunkDraft]:
        drafts: list[ChunkDraft] = []
        current: list[str] = []
        current_words: list[str] = []
        current_section: str | None = None

        for block in blocks:
            words = block.text.split()
            if not words:
                continue
            if len(words) > self.chunk_size_words:
                if current:
                    drafts.append(self._draft(current, page_number, current_section))
                    current, current_words = [], []
                drafts.extend(self._split_long_block(block, page_number))
                current_section = block.section
                continue
            if current and len(current_words) + len(words) > self.chunk_size_words:
                drafts.append(self._draft(current, page_number, current_section))
                overlap = current_words[-self.overlap_words:] if self.overlap_words else []
                current = [" ".join(overlap)] if overlap else []
                current_words = overlap
            if block.section:
                current_section = block.section
            current.append(block.text)
            current_words.extend(words)
        if current:
            drafts.append(self._draft(current, page_number, current_section))
        return drafts

    def _split_long_block(self, block: ExtractedBlock, page_number: int | None) -> list[ChunkDraft]:
        words = block.text.split()
        drafts: list[ChunkDraft] = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size_words, len(words))
            text = " ".join(words[start:end])
            drafts.append(self._draft([text], page_number, block.section))
            if end == len(words):
                break
            start = end - self.overlap_words
        return drafts

    @staticmethod
    def _draft(parts: list[str], page_number: int | None, section: str | None) -> ChunkDraft:
        text = "\n\n".join(parts).strip()
        return ChunkDraft(text, page_number, section, len(text.split()), len(text))
