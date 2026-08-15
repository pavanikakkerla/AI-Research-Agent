from fastapi import APIRouter
from pydantic import BaseModel

from agents.orchestrator import Orchestrator

router = APIRouter()


# ==========================================================
# Initialize Research Pipeline
# ==========================================================

orchestrator = Orchestrator()


# ==========================================================
# Request Models
# ==========================================================

class ResearchRequest(BaseModel):

    query: str

    max_results: int = 5


# ==========================================================
# Home
# ==========================================================

@router.get("/")
async def home():

    return {

        "message": "Research Assistant API",

        "version": "2.0.0",

        "status": "Running"

    }


# ==========================================================
# Health
# ==========================================================

@router.get("/health")
async def health():

    return {

        "status": "healthy"

    }


# ==========================================================
# Research Endpoint
# ==========================================================

@router.post("/research")
async def research(
        request: ResearchRequest
):

    # ------------------------------------------------------
    # Run existing research pipeline
    # ------------------------------------------------------

    result = await orchestrator.research(

        query=request.query,

        max_results=request.max_results

    )

    # ------------------------------------------------------
    # Add Conclusion
    #
    # The existing ReportAgent already generates the report.
    # We simply expose its conclusion in the API response.
    # ------------------------------------------------------

    if isinstance(result, dict):

        # If the orchestrator/report already provides
        # a conclusion, keep it unchanged.

        if "conclusion" not in result:

            report = result.get(
                "report",
                ""
            )

            conclusion = ""

            if isinstance(report, str):

                lines = report.splitlines()

                inside_conclusion = False

                conclusion_lines = []

                for line in lines:

                    stripped = line.strip()

                    # Start of Conclusion section
                    if stripped.lower() in {
                        "## conclusion",
                        "### conclusion",
                        "**conclusion**",
                        "conclusion:"
                    }:

                        inside_conclusion = True

                        continue

                    # Stop at the next markdown section
                    if inside_conclusion:

                        if (
                                stripped.startswith("## ")
                                or stripped.startswith("### ")
                        ):

                            break

                        if stripped:

                            conclusion_lines.append(
                                stripped
                            )

                conclusion = " ".join(
                    conclusion_lines
                ).strip()

            result["conclusion"] = conclusion

    # ------------------------------------------------------
    # Return existing response
    # ------------------------------------------------------

    return result