"""
Embedding Agent

Responsibilities:
- Load embedding model only once
- Generate embeddings for text
- Generate embeddings for batches
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL
from utils.logger import logger


class EmbeddingAgent:
    """
    Singleton Embedding Model
    """

    _model = None

    def __init__(self):

        if EmbeddingAgent._model is None:

            logger.info(
                f"Loading embedding model: {EMBEDDING_MODEL}"
            )

            EmbeddingAgent._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

            logger.info("Embedding model loaded.")

        self.model = EmbeddingAgent._model

    # ---------------------------------------------------
    # Single Embedding
    # ---------------------------------------------------

    def embed(
            self,
            text: str
    ) -> np.ndarray:

        if not text:
            return np.array([], dtype=np.float32)

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding.astype(np.float32)

    # ---------------------------------------------------
    # Batch Embedding
    # ---------------------------------------------------

    def embed_chunks(
            self,
            chunks: List[str]
    ) -> np.ndarray:

        if not chunks:
            return np.array([], dtype=np.float32)

        embeddings = self.model.encode(
            chunks,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings.astype(np.float32)

    # ---------------------------------------------------
    # Embedding Dimension
    # ---------------------------------------------------

    def dimension(self):

        sample = self.embed("Hello")

        return len(sample)