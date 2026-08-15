"""
Orchestrator

Coordinates the complete research pipeline.

Normal Pipeline

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
Report
    ↓
Conclusion


Programming Pipeline

User Query
    ↓
Code Detection
    ↓
Programming Search
    ↓
Scraping
    ↓
Code Extraction
    ↓
Direct Code Response
"""

from agents.search_agent import SearchAgent
from agents.scraper_agent import ScraperAgent
from agents.cleaner_agent import CleanerAgent
from agents.chunker_agent import ChunkerAgent
from agents.embedding_agent import EmbeddingAgent
from agents.retriever_agent import RetrieverAgent
from agents.reranker_agent import RerankerAgent
from agents.summarizer_agent import SummarizerAgent
from agents.report_agent import ReportAgent
from agents.conclusion_agent import ConclusionAgent
from agents.code_agent import CodeAgent

from memory.vectordb import VectorDB

from config import TOP_K

from utils.logger import logger


class Orchestrator:

    def __init__(self):

        logger.info("=" * 80)
        logger.info("Initializing Research Assistant")
        logger.info("=" * 80)

        # =====================================================
        # Core Agents
        # =====================================================

        self.search_agent = SearchAgent()

        self.scraper_agent = ScraperAgent()

        self.cleaner_agent = CleanerAgent()

        self.chunker_agent = ChunkerAgent()

        # =====================================================
        # Embedding
        # =====================================================

        self.embedding_agent = EmbeddingAgent()

        embedding_dimension = (
            self.embedding_agent.dimension()
        )

        logger.info(
            f"Embedding Dimension : "
            f"{embedding_dimension}"
        )

        # =====================================================
        # Vector Database
        # =====================================================

        self.vector_db = VectorDB(
            dimension=embedding_dimension
        )

        # =====================================================
        # Retrieval
        # =====================================================

        self.retriever_agent = RetrieverAgent(
            embedder=self.embedding_agent,
            vector_db=self.vector_db
        )

        self.reranker_agent = RerankerAgent()

        # =====================================================
        # Output
        # =====================================================

        self.summarizer_agent = SummarizerAgent()

        self.report_agent = ReportAgent()

        self.conclusion_agent = ConclusionAgent()

        # =====================================================
        # Code Agent
        # =====================================================

        self.code_agent = CodeAgent()

        logger.info(
            "Research Assistant Ready."
        )

    # =========================================================
    # Research
    # =========================================================

    async def research(
            self,
            query: str,
            max_results: int = 5
    ):

        logger.info("=" * 80)

        logger.info(
            f"Research Started : {query}"
        )

        logger.info("=" * 80)

        # =====================================================
        # CODE MODE
        # =====================================================

        if self.code_agent.is_code_query(
                query
        ):

            logger.info(
                "Programming request detected."
            )

            return await self._research_code(
                query=query,
                max_results=max_results
            )

        # =====================================================
        # NORMAL RESEARCH MODE
        # =====================================================

        return await self._research_general(
            query=query,
            max_results=max_results
        )

    # =========================================================
    # CODE RESEARCH
    # =========================================================

    async def _research_code(
            self,
            query: str,
            max_results: int
    ):

        logger.info(
            "=" * 80
        )

        logger.info(
            "Starting CODE research pipeline."
        )

        logger.info(
            "=" * 80
        )

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

        search_result = self.search_agent.search(
            query=query,
            max_results=max_results
        )

        if not search_result["success"]:

            logger.error(
                "Programming search failed."
            )

            return {
                "success": False,
                "type": "code",
                "query": query,
                "error": search_result.get(
                    "error",
                    "Programming search failed."
                )
            }

        results = search_result[
            "results"
        ]

        if not results:

            return {
                "success": False,
                "type": "code",
                "query": query,
                "error": (
                    "No programming sources "
                    "were found."
                )
            }

        logger.info(
            f"Programming search returned "
            f"{len(results)} results."
        )

        # -----------------------------------------------------
        # URLs
        # -----------------------------------------------------

        urls = [
            result["url"]
            for result in results
            if result.get("url")
        ]

        logger.info(
            f"Scraping {len(urls)} "
            f"programming sources..."
        )

        # -----------------------------------------------------
        # Scrape
        # -----------------------------------------------------

        scraped_pages = (
            await self.scraper_agent.scrape_multiple(
                urls
            )
        )

        logger.info(
            "Finished programming source scraping."
        )

        # -----------------------------------------------------
        # Build direct code response
        # -----------------------------------------------------

        result = self.code_agent.build_response(
            query=query,
            results=results,
            scraped_pages=scraped_pages
        )

        logger.info(
            "Code research completed."
        )

        return result

    # =========================================================
    # GENERAL RESEARCH
    # =========================================================

    async def _research_general(
            self,
            query: str,
            max_results: int
    ):

        logger.info(
            "Starting GENERAL research pipeline."
        )

        # =====================================================
        # Search
        # =====================================================

        search_result = self.search_agent.search(
            query=query,
            max_results=max_results
        )

        if not search_result["success"]:

            return search_result

        results = search_result[
            "results"
        ]

        if not results:

            return {
                "success": False,
                "error": "No search results found."
            }

        logger.info(
            f"Search returned "
            f"{len(results)} results."
        )

        # =====================================================
        # Clear Vector Database
        # =====================================================

        self.vector_db.clear()

        # =====================================================
        # Parallel Scraping
        # =====================================================

        urls = [
            result["url"]
            for result in results
        ]

        logger.info(
            f"Scraping {len(urls)} pages concurrently..."
        )

        scraped_pages = (
            await self.scraper_agent.scrape_multiple(
                urls
            )
        )

        logger.info(
            "Finished scraping."
        )

        # =====================================================
        # Build Page Objects
        # =====================================================

        page_objects = []

        for result, page in zip(
                results,
                scraped_pages
        ):

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
                "error": (
                    "No pages could be scraped."
                )
            }

        logger.info(
            f"Successfully scraped "
            f"{len(page_objects)} pages."
        )

        total_chunks = 0

        # =====================================================
        # Clean → Chunk → Embed
        # =====================================================

        for page in page_objects:

            cleaned = (
                self.cleaner_agent.clean(
                    page["content"]
                )
            )

            if not cleaned:
                continue

            chunks = (
                self.chunker_agent.chunk(
                    cleaned
                )
            )

            if not chunks:
                continue

            embeddings = (
                self.embedding_agent.embed_chunks(
                    chunks
                )
            )

            # -------------------------------------------------
            # Store in Vector Database
            # -------------------------------------------------

            for chunk, embedding in zip(
                    chunks,
                    embeddings
            ):

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
                "error": (
                    "No usable content found."
                )
            }

        # =====================================================
        # Retrieve
        # =====================================================

        logger.info(
            "Retrieving relevant chunks..."
        )

        retrieved_docs = (
            self.retriever_agent.retrieve(
                query=query,
                top_k=TOP_K
            )
        )

        if not retrieved_docs:

            return {
                "success": False,
                "error": (
                    "Retriever returned no documents."
                )
            }

        logger.info(
            f"Retriever selected "
            f"{len(retrieved_docs)} chunks."
        )

        # =====================================================
        # Rerank
        # =====================================================

        logger.info(
            "Reranking retrieved chunks..."
        )

        reranked_docs = (
            self.reranker_agent.rerank(
                query=query,
                documents=retrieved_docs,
                top_k=TOP_K
            )
        )

        if not reranked_docs:

            return {
                "success": False,
                "error": (
                    "Reranker returned no documents."
                )
            }

        logger.info(
            f"Top {len(reranked_docs)} "
            f"chunks selected."
        )

        # =====================================================
        # Summarize
        # =====================================================

        logger.info(
            "Generating summary..."
        )

        summaries = (
            self.summarizer_agent
            .summarize_documents(
                reranked_docs,
                query=query,
                max_sentences=15
            )
        )

        # =====================================================
        # Report
        # =====================================================

        logger.info(
            "Building research report..."
        )

        report = (
            self.report_agent.build_report(
                query=query,
                summaries=summaries,
                retrieved_docs=reranked_docs
            )
        )

        # =====================================================
        # Conclusion
        # =====================================================

        logger.info(
            "Generating conclusion..."
        )

        conclusion = (
            self.conclusion_agent.generate(
                query=query,
                report=report,
                retrieved_docs=reranked_docs
            )
        )

        logger.info(
            "Research Completed"
        )

        # =====================================================
        # Final Response
        # =====================================================

        return {
            "success": True,
            "type": "research",
            "query": query,
            "summary": report["summary"],
            "report": report,
            "conclusion": conclusion,
            "statistics": {
                "search_results": len(results),
                "pages_scraped": len(page_objects),
                "chunks_created": total_chunks,
                "chunks_retrieved": len(
                    retrieved_docs
                ),
                "chunks_reranked": len(
                    reranked_docs
                )
            }
        }

    # =========================================================
    # Cleanup
    # =========================================================

    async def close(self):

        """
        Close async resources.
        """

        await self.scraper_agent.close()