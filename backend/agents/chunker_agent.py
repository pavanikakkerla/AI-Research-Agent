"""
Chunker Agent

Responsibilities:
- Split large documents into semantic chunks
- Preserve sentence boundaries whenever possible
- Add configurable overlap between chunks
"""

import re

from config import CHUNK_SIZE, CHUNK_OVERLAP
from utils.logger import logger


class ChunkerAgent:

    def __init__(
            self,
            chunk_size: int = CHUNK_SIZE,
            overlap: int = CHUNK_OVERLAP
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def _split_sentences(self, text: str):
        """
        Split text into sentences.
        """
        text = text.strip()

        if not text:
            return []

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

    def chunk(self, text: str):

        if not text:
            return []

        logger.info("Creating semantic chunks...")

        sentences = self._split_sentences(text)

        chunks = []

        current_chunk = []

        current_length = 0

        for sentence in sentences:

            sentence_length = len(sentence)

            # If adding this sentence exceeds chunk size,
            # save current chunk.
            if current_chunk and (
                    current_length + sentence_length > self.chunk_size
            ):

                chunk = " ".join(current_chunk)

                chunks.append(chunk)

                # ----------------------------
                # Build overlap
                # ----------------------------

                overlap_sentences = []

                overlap_length = 0

                for s in reversed(current_chunk):

                    overlap_sentences.insert(0, s)

                    overlap_length += len(s)

                    if overlap_length >= self.overlap:
                        break

                current_chunk = overlap_sentences

                current_length = sum(
                    len(s)
                    for s in current_chunk
                )

            current_chunk.append(sentence)

            current_length += sentence_length

        # Last chunk

        if current_chunk:

            chunks.append(
                " ".join(current_chunk)
            )

        logger.info(
            f"Created {len(chunks)} chunks."
        )

        return chunks