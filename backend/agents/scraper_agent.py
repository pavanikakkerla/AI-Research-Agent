"""
Async Scraper Agent

Features:
- Reuses one AsyncClient (connection pooling)
- Parallel scraping support
- SQLite cache
- Retry mechanism
- Trafilatura extraction
- BeautifulSoup fallback
"""

import asyncio
import httpx
import trafilatura

from bs4 import BeautifulSoup

from config import (
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    USER_AGENT
)

from memory.cache import Cache
from utils.logger import logger


class ScraperAgent:

    def __init__(self):

        self.cache = Cache()

        self.headers = {
            "User-Agent": USER_AGENT
        }

        # Reuse a single HTTP client
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(REQUEST_TIMEOUT),
            headers=self.headers,
            follow_redirects=True,
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=50
            )
        )

        logger.info("Async Scraper initialized.")

    # -------------------------------------------------------

    async def scrape(self, url: str):

        cached = self.cache.get_page(url)

        if cached:

            return {
                "success": True,
                "url": url,
                "content": cached
            }

        html = await self.download(url)

        if html is None:

            return {
                "success": False,
                "url": url,
                "content": ""
            }

        content = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            include_links=False,
            favor_precision=True
        )

        if not content:

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            content = soup.get_text(
                separator=" ",
                strip=True
            )

        if not content:

            return {
                "success": False,
                "url": url,
                "content": ""
            }

        self.cache.save_page(
            url,
            content
        )

        return {
            "success": True,
            "url": url,
            "content": content
        }

    # -------------------------------------------------------

    async def download(self, url):

        for attempt in range(MAX_RETRIES):

            try:

                response = await self.client.get(url)

                response.raise_for_status()

                return response.text

            except Exception as e:

                logger.warning(
                    f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {url}"
                )

                if attempt + 1 < MAX_RETRIES:
                    await asyncio.sleep(1)

        logger.error(f"Failed to scrape {url}")

        return None

    # -------------------------------------------------------

    async def scrape_multiple(self, urls):

        tasks = [
            self.scrape(url)
            for url in urls
        ]

        return await asyncio.gather(*tasks)

    # -------------------------------------------------------

    async def close(self):

        await self.client.aclose()