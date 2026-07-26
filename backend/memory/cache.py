"""
SQLite Cache

Caches:
- Search Results
- Scraped Pages
- Embeddings (future)
- Reports (future)
"""

import sqlite3
import json
import time
from pathlib import Path

from utils.logger import logger


class Cache:

    def __init__(self, db_path="cache.db"):

        Path(db_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.create_tables()

        logger.info("SQLite Cache Ready.")

    # -------------------------------------------------

    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS search_cache(

                                                                  query TEXT PRIMARY KEY,

                                                                  result TEXT,

                                                                  timestamp REAL

                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS page_cache(

                                                                url TEXT PRIMARY KEY,

                                                                content TEXT,

                                                                timestamp REAL

                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS embedding_cache(

                                                                     hash TEXT PRIMARY KEY,

                                                                     embedding BLOB,

                                                                     timestamp REAL

                       )
                       """)

        self.conn.commit()

    # -------------------------------------------------

    def get_search(self, query):

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT result FROM search_cache WHERE query=?",
            (query,)
        )

        row = cursor.fetchone()

        if row:

            logger.info(
                f"Search cache hit: {query}"
            )

            return json.loads(row[0])

        return None

    # -------------------------------------------------

    def save_search(self, query, result):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO search_cache
            VALUES(?,?,?)
            """,
            (
                query,
                json.dumps(result),
                time.time()
            )
        )

        self.conn.commit()

    # -------------------------------------------------

    def get_page(self, url):

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT content FROM page_cache WHERE url=?",
            (url,)
        )

        row = cursor.fetchone()

        if row:

            logger.info(
                f"Page cache hit: {url}"
            )

            return row[0]

        return None

    # -------------------------------------------------

    def save_page(self, url, content):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO page_cache
            VALUES(?,?,?)
            """,
            (
                url,
                content,
                time.time()
            )
        )

        self.conn.commit()

    # -------------------------------------------------

    def clear(self):

        cursor = self.conn.cursor()

        cursor.execute(
            "DELETE FROM search_cache"
        )

        cursor.execute(
            "DELETE FROM page_cache"
        )

        cursor.execute(
            "DELETE FROM embedding_cache"
        )

        self.conn.commit()

        logger.info("Cache cleared.")

    # -------------------------------------------------

    def close(self):

        self.conn.close()