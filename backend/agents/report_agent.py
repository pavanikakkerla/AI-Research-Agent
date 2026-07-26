"""
Report Agent

Responsibilities:
- Convert summaries into a structured research report
- Remove duplicate references
- Export report as Markdown
"""

from datetime import datetime

from utils.logger import logger


class ReportAgent:

    def __init__(self):
        logger.info("Report Agent initialized.")

    # -------------------------------------------------
    # Build Report
    # -------------------------------------------------

    def build_report(
            self,
            query: str,
            summaries: list,
            retrieved_docs: list
    ):

        logger.info("Building research report...")

        # ---------------------------------------------
        # References
        # ---------------------------------------------

        references = []
        seen = set()

        for doc in retrieved_docs:

            url = doc["source"]

            if url in seen:
                continue

            seen.add(url)

            references.append(
                {
                    "title": doc["title"],
                    "url": url
                }
            )

        # ---------------------------------------------
        # Convert summaries to ONE markdown string
        # ---------------------------------------------

        if isinstance(summaries, list):

            cleaned = []

            for item in summaries:

                if isinstance(item, str):
                    cleaned.append(item.strip())

                elif isinstance(item, dict):

                    cleaned.append(
                        item.get("summary")
                        or item.get("text")
                        or str(item)
                    )

                else:
                    cleaned.append(str(item))

            summary_text = "\n\n".join(cleaned)

        else:

            summary_text = str(summaries)

        report = {

            "title": f"Research Report: {query}",

            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "query": query,

            # <-- IMPORTANT
            "summary": summary_text,

            "references": references

        }

        logger.info("Report generated.")

        return report

    # -------------------------------------------------
    # Markdown
    # -------------------------------------------------

    def to_markdown(self, report):

        markdown = []

        markdown.append(f"# {report['title']}\n")

        markdown.append(
            f"**Generated:** {report['generated_at']}\n"
        )

        markdown.append(
            f"**Query:** {report['query']}\n"
        )

        markdown.append("## Summary\n")

        markdown.append(report["summary"])

        markdown.append("\n\n## References\n")

        for reference in report["references"]:

            markdown.append(
                f"- [{reference['title']}]({reference['url']})"
            )

        return "\n".join(markdown)