"""
Search Agent

Responsibilities:
- Search the web
- Detect programming queries
- Optimize programming searches
- Prefer programming sources
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

        logger.info(
            "Search Agent initialized."
        )

    # =========================================================
    # Detect Programming Query
    # =========================================================

    def _is_code_query(
            self,
            query: str
    ) -> bool:

        q = query.lower()

        keywords = [
            "code",
            "coding",
            "program",
            "programming",
            "python",
            "javascript",
            "java",
            "c++",
            "c#",
            "html",
            "css",
            "sql",
            "typescript",
            "php",
            "rust",
            "golang",
            "algorithm",
            "function",
            "class",
            "script",
            "leetcode",
            "implement",
            "write code",
            "give me code",
            "show me code",
            "example code",
            "syntax",
            "debug",
        ]

        return any(
            keyword in q
            for keyword in keywords
        )

    # =========================================================
    # Build Search Queries
    # =========================================================

    def _build_queries(
            self,
            query: str
    ):

        if not self._is_code_query(query):

            return [query]

        logger.info(
            "Coding query detected. "
            "Optimizing search for programming sources."
        )

        base = query.strip()

        return [
            f"{base} W3Schools",
            f"{base} Programiz",
            f"{base} GeeksforGeeks",
            f"{base} Python documentation",
        ]

    # =========================================================
    # Search
    # =========================================================

    def search(
            self,
            query: str,
            max_results: int = MAX_RESULTS
    ):

        logger.info(
            f"Searching: {query}"
        )

        # -----------------------------------------------------
        # Cache
        # -----------------------------------------------------

        cached = self.cache.get_search(
            query
        )

        if cached:

            logger.info(
                "Returning cached search results."
            )

            return {
                "success": True,
                "results": cached
            }

        # -----------------------------------------------------
        # Query mode
        # -----------------------------------------------------

        is_code = self._is_code_query(
            query
        )

        if is_code:

            logger.info(
                "Search mode: PROGRAMMING / CODE"
            )

        # -----------------------------------------------------
        # Search
        # -----------------------------------------------------

        results = []

        queries = self._build_queries(
            query
        )

        try:

            # Use the current DDGS automatic backend selection
            # instead of manually forcing providers that may have
            # changed or disappeared.

            with DDGS(timeout=20) as ddgs:

                for search_query in queries:

                    logger.info(
                        f"Search query: {search_query}"
                    )

                    try:

                        current_results = list(
                            ddgs.text(
                                search_query,
                                max_results=max_results,
                            )
                        )

                        if current_results:

                            logger.info(
                                f"Found "
                                f"{len(current_results)} "
                                f"results."
                            )

                            results.extend(
                                current_results
                            )

                    except Exception as error:

                        logger.warning(
                            f"Search failed for "
                            f"'{search_query}': "
                            f"{error}"
                        )

            # -------------------------------------------------
            # If nothing found
            # -------------------------------------------------

            if not results:

                raise RuntimeError(
                    "No search results were returned. "
                    "The search provider may be unavailable "
                    "or network/DNS access may be blocked."
                )

        except Exception as error:

            logger.error(
                f"Search Error: {error}"
            )

            return {
                "success": False,
                "results": [],
                "error": str(error)
            }

        # =====================================================
        # Clean Results
        # =====================================================

        cleaned = []

        seen = set()

        for item in results:

            url = item.get(
                "href"
            )

            if not url:
                continue

            # Normalize URL
            url = url.strip()

            if url in seen:
                continue

            seen.add(url)

            cleaned.append(
                {
                    "title": item.get(
                        "title",
                        ""
                    ),
                    "url": url,
                    "body": item.get(
                        "body",
                        ""
                    )
                }
            )

        # =====================================================
        # Prioritize Programming Sources
        # =====================================================

        if is_code:

            preferred_domains = [
                "w3schools.com",
                "programiz.com",
                "geeksforgeeks.org",
                "docs.python.org",
                "developer.mozilla.org",
                "realpython.com",
                "tutorialspoint.com",
                "freecodecamp.org",
            ]

            def source_priority(item):

                url = item[
                    "url"
                ].lower()

                for index, domain in enumerate(
                        preferred_domains
                ):

                    if domain in url:

                        return index

                return 999

            cleaned.sort(
                key=source_priority
            )

        # -----------------------------------------------------
        # Limit results
        # -----------------------------------------------------

        cleaned = cleaned[
            :max_results
        ]

        logger.info(
            f"Found {len(cleaned)} "
            f"unique results."
        )

        # =====================================================
        # Cache
        # =====================================================

        self.cache.save_search(
            query,
            cleaned
        )

        return {
            "success": True,
            "results": cleaned
        }

    # =========================================================
    # Clear Cache
    # =========================================================

    def clear_cache(self):

        self.cache.clear()