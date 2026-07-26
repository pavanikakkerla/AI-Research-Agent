"""
Retriever Agent

Responsibilities:
- Convert user query into an embedding
- Search the FAISS vector database
- Remove duplicate chunks
"""

from typing import List

from config import TOP_K
from utils.logger import logger


class RetrieverAgent:

    def __init__(
            self,
            embedder,
            vector_db
    ):
        self.embedder = embedder
        self.vector_db = vector_db

    # ---------------------------------------------------
    # Retrieve Documents
    # ---------------------------------------------------

    def retrieve(
            self,
            query: str,
            top_k: int = TOP_K
    ) -> List[dict]:

        if not query.strip():
            return []

        logger.info(f"Retrieving documents for: {query}")

        # Generate embedding
        query_embedding = self.embedder.embed(query)

        # Search Vector DB
        results = self.vector_db.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        # Remove duplicate chunks
        unique_results = []
        seen_chunks = set()

        for result in results:

            chunk = result["chunk"]

            if chunk in seen_chunks:
                continue

            seen_chunks.add(chunk)
            unique_results.append(result)

        logger.info(
            f"Retrieved {len(unique_results)} unique documents."
        )

        return unique_results