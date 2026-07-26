"""
Vector Database using FAISS.

Responsibilities:
- Store embeddings
- Perform fast semantic search
- Save/load index
- Store metadata separately
"""

from pathlib import Path
import pickle

import faiss
import numpy as np

from utils.logger import logger


class VectorDB:

    def __init__(
            self,
            dimension: int = 384,
            index_path: str = "memory/vector.index",
            metadata_path: str = "memory/metadata.pkl"
    ):

        self.dimension = dimension

        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)

        self.index = faiss.IndexFlatIP(self.dimension)

        self.metadata = []

        self.load()

    # -------------------------------------------------
    # Add Document
    # -------------------------------------------------

    def add(
            self,
            chunk: str,
            embedding: np.ndarray,
            source: str,
            title: str
    ):

        embedding = embedding.astype(np.float32)

        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        self.index.add(embedding)

        self.metadata.append(
            {
                "chunk": chunk,
                "source": source,
                "title": title
            }
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
            self,
            query_embedding: np.ndarray,
            top_k: int = 5
    ):

        if self.index.ntotal == 0:
            return []

        query_embedding = query_embedding.astype(np.float32)

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx < 0:
                continue

            doc = self.metadata[idx]

            results.append(
                {
                    "score": float(score),
                    "chunk": doc["chunk"],
                    "source": doc["source"],
                    "title": doc["title"]
                }
            )

        return results

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    def save(self):

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(self.index_path)
        )

        with open(
                self.metadata_path,
                "wb"
        ) as f:

            pickle.dump(
                self.metadata,
                f
            )

        logger.info(
            f"Saved {len(self.metadata)} vectors."
        )

    # -------------------------------------------------
    # Load
    # -------------------------------------------------

    def load(self):

        if self.index_path.exists():

            self.index = faiss.read_index(
                str(self.index_path)
            )

        if self.metadata_path.exists():

            with open(
                    self.metadata_path,
                    "rb"
            ) as f:

                self.metadata = pickle.load(f)

        logger.info(
            f"Loaded {len(self.metadata)} vectors."
        )

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(self):

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.metadata = []

        self.save()

        logger.info("Vector database cleared.")

    # -------------------------------------------------
    # Count
    # -------------------------------------------------

    def count(self):

        return self.index.ntotal