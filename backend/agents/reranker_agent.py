"""
Reranker Agent

Responsibilities:
- Re-rank retrieved documents using a CrossEncoder
- Improve retrieval quality before summarization
"""

from sentence_transformers import CrossEncoder

from config import RERANKER_MODEL
from utils.logger import logger


class RerankerAgent:
    """
    Singleton CrossEncoder reranker.
    """

    _model = None

    def __init__(self):

        if RerankerAgent._model is None:

            logger.info(
                f"Loading reranker model: {RERANKER_MODEL}"
            )

            RerankerAgent._model = CrossEncoder(
                RERANKER_MODEL
            )

            logger.info("Reranker model loaded.")

        self.model = RerankerAgent._model

    # -------------------------------------------------------
    # Re-rank Retrieved Documents
    # -------------------------------------------------------

    def rerank(
            self,
            query: str,
            documents: list,
            top_k: int = 5
    ):

        if not documents:
            return []

        logger.info(
            f"Reranking {len(documents)} documents..."
        )

        sentence_pairs = [
            (query, doc["chunk"])
            for doc in documents
        ]

        scores = self.model.predict(
            sentence_pairs
        )

        for doc, score in zip(documents, scores):

            doc["rerank_score"] = float(score)

        ranked = sorted(
            documents,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        logger.info(
            f"Top rerank score: {ranked[0]['rerank_score']:.4f}"
        )

        return ranked[:top_k]