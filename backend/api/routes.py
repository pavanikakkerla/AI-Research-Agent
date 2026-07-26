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
async def research(request: ResearchRequest):

    result = await orchestrator.research(
        query=request.query,
        max_results=request.max_results
    )

    return result