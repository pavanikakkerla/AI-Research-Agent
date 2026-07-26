"""
Search Agent

Responsibilities:
- Search the web
- Cache search results
- Remove duplicate URLs
- Return clean metadata
"""

from ddgs import DDGS

from config import MAX_RESULTS
from memory.cache import Cache
from utils.logger import logger


class SearchAgent:

    def __init__(self):
        self.cache = Cache()
        logger.info("Search Agent initialized.")

    # ---------------------------------------------------------

    def search(
            self,
            query: str,
            max_results: int = MAX_RESULTS
    ):

        logger.info(f"Searching: {query}")

        # -------------------------
        # Cache
        # -------------------------

        cached = self.cache.get_search(query)

        if cached:
            logger.info("Returning cached search results.")

            return {
                "success": True,
                "results": cached
            }

        # -------------------------
        # Search
        # -------------------------

        results = []

        try:

            backends = [
                "duckduckgo",
                "bing",
                "brave",
                "yahoo",
            ]

            with DDGS(timeout=20) as ddgs:

                for backend in backends:

                    try:

                        logger.info(f"Trying backend: {backend}")

                        results = list(
                            ddgs.text(
                                query,
                                backend=backend,
                                max_results=max_results,
                            )
                        )

                        if results:
                            logger.info(
                                f"Search succeeded using {backend}"
                            )
                            break

                    except Exception as backend_error:

                        logger.warning(
                            f"{backend} failed: {backend_error}"
                        )

            if not results:
                raise RuntimeError(
                    "All search providers failed."
                )

        except Exception as e:

            logger.error(f"Search Error: {e}")

            return {
                "success": False,
                "results": [],
                "error": str(e)
            }

        # -------------------------
        # Clean Results
        # -------------------------

        cleaned = []
        seen = set()

        for item in results:

            url = item.get("href")

            if not url:
                continue

            if url in seen:
                continue

            seen.add(url)

            cleaned.append({
                "title": item.get("title", ""),
                "url": url,
                "body": item.get("body", "")
            })

        logger.info(f"Found {len(cleaned)} unique results.")

        # -------------------------
        # Cache Results
        # -------------------------

        self.cache.save_search(query, cleaned)

        return {
            "success": True,
            "results": cleaned
        }

    # ---------------------------------------------------------

    def clear_cache(self):
        self.cache.clear()