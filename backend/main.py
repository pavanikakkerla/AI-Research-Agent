from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router, orchestrator
from config import APP_NAME, VERSION


# =====================================================
# Lifespan
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    yield

    # Shutdown
    await orchestrator.close()


# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    lifespan=lifespan
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =====================================================
# API Routes
# =====================================================

app.include_router(router)


# =====================================================
# Root
# =====================================================

@app.get("/")
async def root():

    return {
        "message": APP_NAME,
        "version": VERSION,
        "status": "Running"
    }