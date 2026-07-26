"""
Cleaner Agent

Responsibilities:
- Remove citations
- Remove extra whitespace
- Remove boilerplate text
- Normalize unicode characters
- Remove duplicate lines
"""

import re
import unicodedata

from utils.logger import logger


class CleanerAgent:

    def __init__(self):

        self.boilerplate_patterns = [

            r"cookie policy",
            r"accept cookies",
            r"privacy policy",
            r"terms of service",
            r"all rights reserved",
            r"subscribe",
            r"sign in",
            r"log in",
            r"advertisement",
            r"advertising",
            r"newsletter",
            r"skip to content",
            r"read more",
            r"related articles",
            r"follow us",
            r"share this article",
            r"copyright"
        ]

    def clean(self, text: str) -> str:

        if not text:
            return ""

        logger.info("Cleaning extracted text...")

        # ==========================================
        # Normalize unicode
        # ==========================================

        text = unicodedata.normalize(
            "NFKC",
            text
        )

        # ==========================================
        # Remove citations like:
        # [1] [25] [citation needed]
        # ==========================================

        text = re.sub(
            r"\[[^\]]*\]",
            "",
            text
        )

        # ==========================================
        # Remove URLs
        # ==========================================

        text = re.sub(
            r"http\S+",
            "",
            text
        )

        text = re.sub(
            r"www\.\S+",
            "",
            text
        )

        # ==========================================
        # Remove emails
        # ==========================================

        text = re.sub(
            r"\S+@\S+",
            "",
            text
        )

        # ==========================================
        # Remove boilerplate
        # ==========================================

        lowered = text.lower()

        for pattern in self.boilerplate_patterns:

            lowered = re.sub(
                pattern,
                "",
                lowered,
                flags=re.IGNORECASE
            )

        text = lowered

        # ==========================================
        # Remove duplicate lines
        # ==========================================

        unique_lines = []

        seen = set()

        for line in text.split("\n"):

            line = line.strip()

            if len(line) < 3:
                continue

            if line in seen:
                continue

            seen.add(line)

            unique_lines.append(line)

        text = "\n".join(unique_lines)

        # ==========================================
        # Remove extra spaces
        # ==========================================

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        # ==========================================
        # Remove repeated punctuation
        # ==========================================

        text = re.sub(
            r"\.{2,}",
            ".",
            text
        )

        text = re.sub(
            r"\!{2,}",
            "!",
            text
        )

        text = re.sub(
            r"\?{2,}",
            "?",
            text
        )

        logger.info(
            f"Cleaned text length: {len(text)} characters"
        )

        return text.strip()