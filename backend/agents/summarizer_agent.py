"""
Summarizer Agent

Responsibilities:
- Build a query-aware summary
- Remove duplicate information
- Rank informative sentences
- Preserve logical flow
- Produce a markdown summary
"""

import re

from utils.logger import logger


class SummarizerAgent:

    def __init__(self):
        logger.info("Summarizer initialized.")

    # --------------------------------------------------
    # Split text into sentences
    # --------------------------------------------------

    def split_sentences(self, text):

        sentences = re.split(
            r'(?<=[.!?])\s+',
            text
        )

        cleaned = []

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) < 40:
                continue

            cleaned.append(sentence)

        return cleaned

    # --------------------------------------------------
    # Remove duplicate sentences
    # --------------------------------------------------

    def remove_duplicates(self, sentences):

        unique = []
        seen = set()

        for sentence in sentences:

            key = " ".join(
                sentence.lower().split()
            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(sentence)

        return unique

    # --------------------------------------------------
    # Score a sentence
    # --------------------------------------------------

    def score_sentence(
            self,
            sentence,
            query_words
    ):

        score = 0

        sentence_lower = sentence.lower()

        # ------------------------------------------
        # Query relevance
        # ------------------------------------------

        for word in query_words:

            if len(word) < 3:
                continue

            if word in sentence_lower:
                score += 10

        # ------------------------------------------
        # Prefer informative sentence length
        # ------------------------------------------

        length = len(sentence.split())

        if 12 <= length <= 45:
            score += 5

        # ------------------------------------------
        # Bonus for explanation words
        # ------------------------------------------

        keywords = [

            "is",
            "are",
            "refers",
            "defined",
            "means",
            "because",
            "therefore",
            "important",
            "advantage",
            "advantages",
            "disadvantage",
            "limitations",
            "example",
            "examples",
            "application",
            "applications",
            "used",
            "used for",
            "helps",
            "allows",
            "consists",
            "includes"

        ]

        for keyword in keywords:

            if keyword in sentence_lower:
                score += 2

        # ------------------------------------------
        # Numbers usually indicate facts
        # ------------------------------------------

        if re.search(r"\d", sentence):
            score += 3

        # ------------------------------------------
        # Prefer medium-length informative sentences
        # ------------------------------------------

        if len(sentence) > 250:
            score -= 2

        return score

    # --------------------------------------------------
    # Summarize
    # --------------------------------------------------

    def summarize_documents(
            self,
            documents,
            query="",
            max_sentences=15
    ):

        logger.info(
            f"Summarizing {len(documents)} documents..."
        )

        merged = "\n".join(

            doc["chunk"]

            for doc in documents

            if doc.get("chunk")

        )

        sentences = self.split_sentences(
            merged
        )

        sentences = self.remove_duplicates(
            sentences
        )

        query_words = set(

            re.findall(
                r"\w+",
                query.lower()
            )

        )

        scored = []

        for sentence in sentences:

            score = self.score_sentence(

                sentence,
                query_words

            )

            scored.append(
                (
                    score,
                    sentence
                )
            )

        scored.sort(

            key=lambda x: x[0],
            reverse=True

        )

        selected = [

            sentence

            for _, sentence

            in scored[:max_sentences]

        ]

        # Preserve original order

        ordered = []

        for sentence in sentences:

            if sentence in selected:
                ordered.append(sentence)

        if not ordered:

            return "No useful information could be summarized."

        # ------------------------------------------
        # Build Markdown Report
        # ------------------------------------------

        markdown = []

        markdown.append("### Overview\n")

        markdown.append(
            ordered[0]
        )

        if len(ordered) > 1:

            markdown.append("\n\n### Key Information\n")

            for sentence in ordered[1:]:

                markdown.append(
                    f"- {sentence}"
                )

        logger.info(
            f"Generated summary with {len(ordered)} sentences."
        )

        return "\n".join(markdown)