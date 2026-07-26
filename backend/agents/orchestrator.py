"""
Orchestrator

Coordinates the complete research pipeline.

Pipeline

User Query
    ↓
Search
    ↓
Parallel Async Scraping
    ↓
Cleaning
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Store
    ↓
Retrieval
    ↓
Reranking
    ↓
Summarization
    ↓
Report Generation
"""

import asyncio

from agents.search_agent import SearchAgent
from agents.scraper_agent import ScraperAgent
from agents.cleaner_agent import CleanerAgent
from agents.chunker_agent import ChunkerAgent
from agents.embedding_agent import EmbeddingAgent
from agents.retriever_agent import RetrieverAgent
from agents.reranker_agent import RerankerAgent
from agents.summarizer_agent import SummarizerAgent
from agents.report_agent import ReportAgent

from memory.vectordb import VectorDB

from config import TOP_K

from utils.logger import logger


class Orchestrator:

    def __init__(self):

        logger.info("=" * 80)
        logger.info("Initializing Research Assistant")
        logger.info("=" * 80)

        # --------------------------------------------------
        # Core Agents
        # --------------------------------------------------

        self.search_agent = SearchAgent()
        self.scraper_agent = ScraperAgent()

        self.cleaner_agent = CleanerAgent()
        self.chunker_agent = ChunkerAgent()

        # --------------------------------------------------
        # Embedding
        # --------------------------------------------------

        self.embedding_agent = EmbeddingAgent()

        embedding_dimension = self.embedding_agent.dimension()

        logger.info(
            f"Embedding Dimension : {embedding_dimension}"
        )

        # --------------------------------------------------
        # Vector Database
        # --------------------------------------------------

        self.vector_db = VectorDB(
            dimension=embedding_dimension
        )

        # --------------------------------------------------
        # Retrieval
        # --------------------------------------------------

        self.retriever_agent = RetrieverAgent(
            embedder=self.embedding_agent,
            vector_db=self.vector_db
        )

        self.reranker_agent = RerankerAgent()

        # --------------------------------------------------
        # Output
        # --------------------------------------------------

        self.summarizer_agent = SummarizerAgent()
        self.report_agent = ReportAgent()

        logger.info("Research Assistant Ready.")

    # ======================================================
    # Research
    # ======================================================

    async def research(
            self,
            query: str,
            max_results: int = 5
    ):

        logger.info("=" * 80)
        logger.info(f"Research Started : {query}")
        logger.info("=" * 80)

        # -----------------------------------------------
        # Search
        # -----------------------------------------------

        search_result = self.search_agent.search(
            query=query,
            max_results=max_results
        )

        if not search_result["success"]:

            return search_result

        results = search_result["results"]

        if not results:

            return {
                "success": False,
                "error": "No search results found."
            }

        logger.info(
            f"Search returned {len(results)} results."
        )

        # -----------------------------------------------
        # Clear Vector Database
        # -----------------------------------------------

        self.vector_db.clear()

        # -----------------------------------------------
        # Parallel Scraping
        # -----------------------------------------------

        urls = [
            result["url"]
            for result in results
        ]

        logger.info(
            f"Scraping {len(urls)} pages concurrently..."
        )

        scraped_pages = await self.scraper_agent.scrape_multiple(
            urls
        )

        logger.info(
            "Finished scraping."
        )

        # -----------------------------------------------
        # Build Page Objects
        # -----------------------------------------------

        page_objects = []

        for result, page in zip(results, scraped_pages):

            if not page["success"]:
                continue

            page_objects.append(
                {
                    "title": result["title"],
                    "url": result["url"],
                    "content": page["content"]
                }
            )

        if not page_objects:

            return {
                "success": False,
                "error": "No pages could be scraped."
            }

        logger.info(
            f"Successfully scraped {len(page_objects)} pages."
        )

        total_chunks = 0

        # -----------------------------------------------
        # Clean → Chunk → Embed
        # -----------------------------------------------

        for page in page_objects:

            cleaned = self.cleaner_agent.clean(
                page["content"]
            )

            if not cleaned:
                continue

            chunks = self.chunker_agent.chunk(
                cleaned
            )

            if not chunks:
                continue

            embeddings = self.embedding_agent.embed_chunks(
                chunks
            )

            # -----------------------------------------------
            # Store in Vector Database
            # -----------------------------------------------



            for chunk, embedding in zip(chunks, embeddings):

                self.vector_db.add(
                        chunk=chunk,
                embedding=embedding,
                source=page["url"],
                title=page["title"]
                )



            total_chunks += len(chunks)

        logger.info(
            f"Indexed {total_chunks} chunks."
        )

        if total_chunks == 0:

            return {
                "success": False,
                "error": "No usable content found."
            }

        # --------------------------------------------------
        # Retrieve Relevant Chunks
        # --------------------------------------------------

        logger.info("Retrieving relevant chunks...")

        retrieved_docs = self.retriever_agent.retrieve(
            query=query,
            top_k=TOP_K
        )

        if not retrieved_docs:

            return {
                "success": False,
                "error": "Retriever returned no documents."
            }

        logger.info(
            f"Retriever selected {len(retrieved_docs)} chunks."
        )

        # --------------------------------------------------
        # Rerank
        # --------------------------------------------------

        logger.info("Reranking retrieved chunks...")

        reranked_docs = self.reranker_agent.rerank(
            query=query,
            documents=retrieved_docs,
            top_k=TOP_K
        )

        if not reranked_docs:

            return {
                "success": False,
                "error": "Reranker returned no documents."
            }

        logger.info(
            f"Top {len(reranked_docs)} chunks selected."
        )

        # --------------------------------------------------
        # Summarize
        # --------------------------------------------------

        logger.info("Generating summary...")

        summaries = self.summarizer_agent.summarize_documents(
            reranked_docs,
            query=query,
            max_sentences=15
        )

        # --------------------------------------------------
        # Build Report
        # --------------------------------------------------

        report = self.report_agent.build_report(
            query=query,
            summaries=summaries,
            retrieved_docs=reranked_docs
        )

        logger.info("=" * 80)
        logger.info("Research Completed")
        logger.info("=" * 80)

        return {
            "success": True,
            "query": query,
            "summary": report["summary"],
            "report": report,
            "statistics": {
                "search_results": len(results),
                "pages_scraped": len(page_objects),
                "chunks_created": total_chunks,
                "chunks_retrieved": len(retrieved_docs),
                "chunks_reranked": len(reranked_docs)
            }
        }

    # ======================================================
    # Cleanup
    # ======================================================

    async def close(self):
        """
        Close async resources.
        """
        await self.scraper_agent.close()