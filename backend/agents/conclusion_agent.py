"""
conclusion_agent.py
===================

Conclusion Agent for Neo Research.

Responsibilities
----------------
1. Generate a focused conclusion from research evidence.
2. Keep the conclusion centered on the user's actual topic.
3. Remove irrelevant company/product/source-specific information.
4. Avoid copying unrelated retrieved sentences.
5. Produce a natural, readable conclusion.
6. Preserve the existing research architecture.
"""

from __future__ import annotations

import re
from typing import Any

from utils.logger import logger


class ConclusionAgent:
    """
    Generates a focused conclusion from the existing
    research pipeline.

    This agent does NOT change the architecture.
    It only processes the summary/research evidence
    already produced by the existing agents.
    """

    def __init__(self):
        logger.info("ConclusionAgent initialized.")

    # ==========================================================
    # PUBLIC METHOD
    # ==========================================================

    def generate(
            self,
            query: str,
            summaries: Any = None,
            retrieved_docs: Any = None,
            summary: Any = None,
            documents: Any = None,
            report: Any = None,
            **kwargs
    ) -> str:

        logger.info("Generating research conclusion...")

        query = self._clean_text(query)

        if not query:
            return (
                "The available research does not provide enough "
                "information to produce a meaningful conclusion."
            )

        # ------------------------------------------------------
        # Extract research evidence
        # ------------------------------------------------------

        evidence = self._extract_summary_text(summaries)

        if not evidence:
            evidence = self._extract_summary_text(summary)

        if not evidence:
            evidence = self._extract_documents(retrieved_docs)

        if not evidence:
            evidence = self._extract_documents(documents)

        if not evidence:
            evidence = self._extract_report_text(report)

        if not evidence:
            return self._fallback_conclusion(query)

        # ------------------------------------------------------
        # Clean evidence
        # ------------------------------------------------------

        evidence = self._clean_evidence(evidence)

        if not evidence:
            return self._fallback_conclusion(query)

        # ------------------------------------------------------
        # Identify actual topic
        # ------------------------------------------------------

        topic = self._extract_topic(query)

        # ------------------------------------------------------
        # Detect query type
        # ------------------------------------------------------

        definition_query = self._is_definition_query(query)

        # ------------------------------------------------------
        # Extract sentences
        # ------------------------------------------------------

        sentences = self._split_sentences(evidence)

        if not sentences:
            return self._fallback_conclusion(query)

        # ------------------------------------------------------
        # Remove irrelevant sentences
        # ------------------------------------------------------

        sentences = self._filter_irrelevant_sentences(
            sentences,
            topic=topic,
            query=query
        )

        if not sentences:
            return self._fallback_conclusion(query)

        # ------------------------------------------------------
        # Select relevant evidence
        # ------------------------------------------------------

        selected = self._select_relevant_sentences(
            sentences=sentences,
            topic=topic,
            query=query,
            definition_query=definition_query
        )

        # ------------------------------------------------------
        # Remove duplicates
        # ------------------------------------------------------

        selected = self._remove_duplicates(selected)

        # ------------------------------------------------------
        # Build conclusion
        # ------------------------------------------------------

        conclusion = self._build_conclusion(
            topic=topic,
            query=query,
            sentences=selected,
            definition_query=definition_query
        )

        if not conclusion:
            return self._fallback_conclusion(query)

        logger.info("Research conclusion generated successfully.")

        return conclusion

    # ==========================================================
    # EXTRACT SUMMARY
    # ==========================================================

    def _extract_summary_text(self, summaries: Any) -> str:

        if summaries is None:
            return ""

        if isinstance(summaries, str):
            return summaries

        if isinstance(summaries, list):

            parts = []

            for item in summaries:

                if isinstance(item, str):
                    parts.append(item)
                    continue

                if isinstance(item, dict):

                    for key in (
                            "summary",
                            "text",
                            "content",
                            "description",
                            "key_information"
                    ):

                        value = item.get(key)

                        if isinstance(value, str) and value.strip():
                            parts.append(value)
                            break

            return "\n".join(parts)

        if isinstance(summaries, dict):

            parts = []

            for key in (
                    "summary",
                    "text",
                    "content",
                    "overview",
                    "key_information"
            ):

                value = summaries.get(key)

                if isinstance(value, str):
                    parts.append(value)

                elif isinstance(value, list):

                    for item in value:

                        if isinstance(item, str):
                            parts.append(item)

                        elif isinstance(item, dict):

                            text = (
                                    item.get("summary")
                                    or item.get("text")
                                    or item.get("content")
                            )

                            if isinstance(text, str):
                                parts.append(text)

            return "\n".join(parts)

        return str(summaries)

    # ==========================================================
    # EXTRACT DOCUMENTS
    # ==========================================================

    def _extract_documents(self, documents: Any) -> str:

        if not documents:
            return ""

        if isinstance(documents, str):
            return documents

        if not isinstance(documents, list):
            return str(documents)

        parts = []

        for document in documents:

            if isinstance(document, str):
                parts.append(document)
                continue

            if not isinstance(document, dict):
                continue

            content = (
                    document.get("content")
                    or document.get("text")
                    or document.get("chunk")
                    or document.get("snippet")
                    or document.get("summary")
                    or ""
            )

            if content:
                parts.append(str(content))

        return "\n".join(parts)

    # ==========================================================
    # EXTRACT REPORT
    # ==========================================================

    def _extract_report_text(self, report: Any) -> str:

        if not report:
            return ""

        if isinstance(report, str):
            return report

        if isinstance(report, dict):

            parts = []

            for key in (
                    "summary",
                    "overview",
                    "report",
                    "content",
                    "analysis"
            ):

                value = report.get(key)

                if isinstance(value, str):
                    parts.append(value)

            return "\n".join(parts)

        return str(report)

    # ==========================================================
    # CLEAN TEXT
    # ==========================================================

    def _clean_text(self, text: Any) -> str:

        if text is None:
            return ""

        text = str(text)

        # Remove markdown headings
        text = re.sub(
            r"#{1,6}\s*",
            "",
            text
        )

        # Remove markdown bullets
        text = re.sub(
            r"(?m)^\s*[-*•]+\s*",
            "",
            text
        )

        # Remove numbered-list prefixes
        text = re.sub(
            r"(?m)^\s*\d+[.)]\s*",
            "",
            text
        )

        # Normalize whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ==========================================================
    # CLEAN EVIDENCE
    # ==========================================================

    def _clean_evidence(self, evidence: str) -> str:

        if not evidence:
            return ""

        evidence = re.sub(
            r"#{1,6}\s*",
            "",
            evidence
        )

        evidence = re.sub(
            r"(?m)^\s*[-*•]+\s*",
            "",
            evidence
        )

        evidence = re.sub(
            r"(?m)^\s*\d+[.)]\s*",
            "",
            evidence
        )

        evidence = re.sub(
            r"\s+",
            " ",
            evidence
        )

        return evidence.strip()

    # ==========================================================
    # EXTRACT TOPIC
    # ==========================================================

    def _extract_topic(self, query: str) -> str:

        query = self._clean_text(query)

        patterns = [
            r"^what\s+is\s+(.+?)[?!.]*$",
            r"^what\s+are\s+(.+?)[?!.]*$",
            r"^who\s+is\s+(.+?)[?!.]*$",
            r"^who\s+are\s+(.+?)[?!.]*$",
            r"^define\s+(.+?)[?!.]*$",
            r"^definition\s+of\s+(.+?)[?!.]*$",
            r"^explain\s+(.+?)[?!.]*$",
            r"^tell\s+me\s+about\s+(.+?)[?!.]*$",
            r"^information\s+about\s+(.+?)[?!.]*$",
            r"^research\s+(.+?)[?!.]*$"
        ]

        lower_query = query.lower()

        for pattern in patterns:

            match = re.match(
                pattern,
                lower_query,
                flags=re.IGNORECASE
            )

            if match:

                topic = match.group(1).strip()

                topic = re.sub(
                    r"[?.!]+$",
                    "",
                    topic
                )

                return topic.strip()

        return re.sub(
            r"[?.!]+$",
            "",
            query
        ).strip()

    # ==========================================================
    # QUERY TYPE
    # ==========================================================

    def _is_definition_query(self, query: str) -> bool:

        lower = query.lower().strip()

        return (
                lower.startswith("what is ")
                or lower.startswith("what are ")
                or lower.startswith("define ")
                or lower.startswith("definition of ")
        )

    # ==========================================================
    # SENTENCE SPLITTER
    # ==========================================================

    def _split_sentences(self, text: str) -> list[str]:

        text = text.replace(
            "\n",
            " "
        )

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        result = []

        for sentence in sentences:

            sentence = self._clean_text(sentence)

            if not sentence:
                continue

            if len(sentence.split()) < 7:
                continue

            result.append(sentence)

        return result

    # ==========================================================
    # IRRELEVANT SENTENCE FILTER
    # ==========================================================

    def _filter_irrelevant_sentences(
            self,
            sentences: list[str],
            topic: str,
            query: str
    ) -> list[str]:

        filtered = []

        topic_words = self._topic_words(topic)

        # ------------------------------------------------------
        # These are normally source/company specific and should
        # not dominate a general conceptual conclusion.
        # ------------------------------------------------------

        irrelevant_patterns = [

            # Companies / products
            r"\baws\b",
            r"\bamazon web services\b",
            r"\bgoogle cloud\b",
            r"\bmicrosoft azure\b",
            r"\bgoogle\b",
            r"\bamazon\b",
            r"\bmicrosoft\b",
            r"\bopenai\b",
            r"\bmeta\b",
            r"\bnvidia\b",
            r"\bapple\b",

            # Corporate material
            r"\bceo\b",
            r"\bchief executive\b",
            r"\brevenue\b",
            r"\bprofit\b",
            r"\bstock\b",
            r"\binvestment\b",
            r"\bmarket share\b",

            # Specific competitions
            r"\bicpc\b",
            r"\bworld finals\b",
            r"\b139 teams\b",
            r"\bgold[- ]level\b",
            r"\bgold medal\b",

            # Company marketing
            r"\bbusiness advantage\b",
            r"\benterprise-grade\b",
            r"\bavailable from aws\b",
            r"\baws provides\b",
            r"\bgoogle provides\b"
        ]

        for sentence in sentences:

            lower = sentence.lower()

            # --------------------------------------------------
            # Strongly irrelevant source-specific sentence
            # --------------------------------------------------

            irrelevant = False

            for pattern in irrelevant_patterns:

                if re.search(pattern, lower):

                    # Keep the sentence only if it is clearly
                    # explaining the actual topic.
                    conceptual_words = (
                        "artificial intelligence",
                        "intelligence is",
                        "ai is",
                        "ai refers",
                        "ai systems",
                        "machine learning",
                        "reasoning",
                        "learning",
                        "problem solving"
                    )

                    if not any(
                            phrase in lower
                            for phrase in conceptual_words
                    ):
                        irrelevant = True
                        break

            if irrelevant:
                continue

            # --------------------------------------------------
            # Require some connection to the topic.
            # --------------------------------------------------

            if topic_words:

                matches = sum(
                    1
                    for word in topic_words
                    if re.search(
                        rf"\b{re.escape(word)}\b",
                        lower
                    )
                )

                # For AI, allow its conceptual vocabulary.
                if matches == 0:

                    if not self._contains_conceptual_ai_terms(lower):
                        continue

            filtered.append(sentence)

        return filtered

    # ==========================================================
    # TOPIC WORDS
    # ==========================================================

    def _topic_words(self, topic: str) -> set[str]:

        words = re.findall(
            r"[a-zA-Z0-9]+",
            topic.lower()
        )

        stop_words = {
            "what",
            "is",
            "are",
            "the",
            "a",
            "an",
            "of",
            "in",
            "on",
            "for",
            "to",
            "and",
            "or",
            "about",
            "explain",
            "definition",
            "define"
        }

        return {
            word
            for word in words
            if len(word) >= 2
               and word not in stop_words
        }

    # ==========================================================
    # AI CONCEPT CHECK
    # ==========================================================

    def _contains_conceptual_ai_terms(self, text: str) -> bool:

        terms = [
            "artificial intelligence",
            "artificial system",
            "ai system",
            "ai systems",
            "machine intelligence",
            "human intelligence",
            "reasoning",
            "learning",
            "problem solving",
            "problem-solving",
            "decision making",
            "decision-making",
            "perception",
            "planning",
            "cognition",
            "autonomy",
            "neural network",
            "machine learning",
            "deep learning"
        ]

        return any(
            term in text
            for term in terms
        )

    # ==========================================================
    # RELEVANCE SELECTION
    # ==========================================================

    def _select_relevant_sentences(
            self,
            sentences: list[str],
            topic: str,
            query: str,
            definition_query: bool
    ) -> list[str]:

        topic_words = self._topic_words(topic)

        scored = []

        for index, sentence in enumerate(sentences):

            lower = sentence.lower()

            score = 0

            # --------------------------------------------------
            # Topic matches
            # --------------------------------------------------

            for word in topic_words:

                if re.search(
                        rf"\b{re.escape(word)}\b",
                        lower
                ):
                    score += 5

            # --------------------------------------------------
            # Definition language
            # --------------------------------------------------

            definition_terms = [
                "is",
                "are",
                "refers to",
                "defined as",
                "means",
                "designed to",
                "capable of",
                "enables",
                "allows"
            ]

            for term in definition_terms:

                if re.search(
                        rf"\b{re.escape(term)}\b",
                        lower
                ):
                    score += 3

            # --------------------------------------------------
            # Core AI concepts
            # --------------------------------------------------

            core_terms = [
                "learning",
                "reasoning",
                "problem solving",
                "problem-solving",
                "decision making",
                "decision-making",
                "perception",
                "planning",
                "prediction",
                "pattern",
                "cognition",
                "autonomy",
                "human intelligence"
            ]

            for term in core_terms:

                if term in lower:
                    score += 2

            # --------------------------------------------------
            # Definition questions strongly prefer definitions.
            # --------------------------------------------------

            if definition_query:

                if any(
                        phrase in lower
                        for phrase in (
                                "artificial intelligence is",
                                "artificial intelligence refers",
                                "ai is",
                                "ai refers",
                                "artificial system",
                                "systems capable of"
                        )
                ):
                    score += 10

            # --------------------------------------------------
            # Prefer reasonably concise sentences.
            # --------------------------------------------------

            word_count = len(sentence.split())

            if 10 <= word_count <= 45:
                score += 2

            if word_count > 70:
                score -= 3

            scored.append(
                (
                    score,
                    index,
                    sentence
                )
            )

        # Highest relevance first
        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        selected = []

        for score, _, sentence in scored:

            if score <= 0:
                continue

            selected.append(sentence)

            if len(selected) >= 6:
                break

        # Restore natural source order
        selected_set = set(selected)

        return [
            sentence
            for sentence in sentences
            if sentence in selected_set
        ]

    # ==========================================================
    # REMOVE DUPLICATES
    # ==========================================================

    def _remove_duplicates(
            self,
            sentences: list[str]
    ) -> list[str]:

        unique = []
        seen = set()

        for sentence in sentences:

            normalized = re.sub(
                r"[^a-z0-9]",
                "",
                sentence.lower()
            )

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(normalized)

            unique.append(sentence)

        return unique

    # ==========================================================
    # BUILD CONCLUSION
    # ==========================================================

    def _build_conclusion(
            self,
            topic: str,
            query: str,
            sentences: list[str],
            definition_query: bool
    ) -> str:

        if not sentences:
            return self._fallback_conclusion(query)

        # ------------------------------------------------------
        # For "What is..." questions:
        #
        # Do NOT generate:
        # "Overall, the research shows that What is AI?..."
        #
        # Instead explain the topic directly.
        # ------------------------------------------------------

        if definition_query:

            body = " ".join(
                sentences[:4]
            )

            body = self._clean_text(body)

            body = self._remove_bad_opening(body)

            if not body:
                return self._fallback_conclusion(query)

            conclusion = (
                f"Overall, {topic} refers to "
                f"{self._normalize_definition_body(body)}"
            )

            conclusion = self._clean_final_conclusion(
                conclusion
            )

            return conclusion

        # ------------------------------------------------------
        # General research questions
        # ------------------------------------------------------

        body = " ".join(
            sentences[:4]
        )

        body = self._clean_text(body)

        body = self._remove_bad_opening(body)

        if not body:
            return self._fallback_conclusion(query)

        conclusion = (
            f"Overall, the research indicates that "
            f"{topic} is characterized by {body}"
        )

        conclusion = self._clean_final_conclusion(
            conclusion
        )

        return conclusion

    # ==========================================================
    # NORMALIZE DEFINITION
    # ==========================================================

    def _normalize_definition_body(
            self,
            body: str
    ) -> str:

        body = body.strip()

        # Remove repeated introductory phrases.
        prefixes = [
            "artificial intelligence is",
            "artificial intelligence refers to",
            "ai is",
            "ai refers to",
            "overall",
            "in conclusion",
            "taken together"
        ]

        lower = body.lower()

        for prefix in prefixes:

            if lower.startswith(prefix):

                body = body[len(prefix):].strip()

                if body:
                    body = body[0].lower() + body[1:]

                break

        # Remove leading punctuation.
        body = re.sub(
            r"^[,:;\-–—\s]+",
            "",
            body
        )

        return body

    # ==========================================================
    # REMOVE BAD OPENING
    # ==========================================================

    def _remove_bad_opening(
            self,
            text: str
    ) -> str:

        text = re.sub(
            r"^(overall|in conclusion|taken together)[,:]?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"^(the research (shows|indicates|suggests))"
            r"[,:]?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        return text.strip()

    # ==========================================================
    # FINAL CLEANUP
    # ==========================================================

    def _clean_final_conclusion(
            self,
            text: str
    ) -> str:

        text = self._clean_text(text)

        # Remove accidental duplicate spaces.
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        # Remove duplicated punctuation.
        text = re.sub(
            r"\.{2,}",
            ".",
            text
        )

        # Remove repeated phrases.
        text = re.sub(
            r"\boverall,\s+overall,\s+",
            "Overall, ",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\bthe research shows that\s+the research shows that\b",
            "the research shows that",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\bthe research indicates that\s+the research indicates that\b",
            "the research indicates that",
            text,
            flags=re.IGNORECASE
        )

        return text.strip()

    # ==========================================================
    # FALLBACK
    # ==========================================================

    def _fallback_conclusion(
            self,
            query: str
    ) -> str:

        topic = self._extract_topic(query)

        if not topic:
            topic = "the topic"

        return (
            f"The available research provides relevant information "
            f"about {topic}, but the retrieved evidence is not "
            f"sufficient to produce a more specific conclusion."
        )

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health(self) -> dict:

        return {
            "service": "ConclusionAgent",
            "status": "healthy"
        }


# ==============================================================
# LOCAL TEST
# ==============================================================

if __name__ == "__main__":

    agent = ConclusionAgent()

    test_query = "What is AI?"

    test_summary = """
    Artificial intelligence is the field of computer science
    concerned with creating systems capable of performing tasks
    that normally require human intelligence.

    AI systems can perform tasks involving reasoning,
    learning, problem solving, perception and decision making.

    Artificial intelligence can be applied across healthcare,
    finance, transportation, education and many other fields.

    AI agents are software systems that can perceive their
    environment and take actions to achieve specific goals.

    AWS provides cloud services for developing AI applications.

    Google has invested heavily in artificial intelligence
    research and development.
    """

    result = agent.generate(
        query=test_query,
        summaries=test_summary
    )

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print(result)