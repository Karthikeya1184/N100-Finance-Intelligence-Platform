from pathlib import Path
import sqlite3
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import (
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents,
    health,
)


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="N100 Finance Intelligence Platform API",
    version="1.0.0",
    description="Sprint 6 FastAPI Backend"
)


# ============================================================
# Database Connection
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def get_connection():

    return sqlite3.connect(DB_PATH)


# ============================================================
# CORS Middleware
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Logging Middleware
# ============================================================

@app.middleware("http")
async def log_requests(request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{elapsed_ms:.2f} ms"
    )

    return response



app.include_router(
    companies.router,
    prefix="/api/v1/companies",
    tags=["Companies"],
)

app.include_router(
    screener.router,
    prefix="/api/v1/screener",
    tags=["Screener"],
)

app.include_router(
    sectors.router,
    prefix="/api/v1/sectors",
    tags=["Sectors"],
)

app.include_router(
    peers.router,
    prefix="/api/v1/peers",
    tags=["Peers"],
)

app.include_router(
    valuation.router,
    prefix="/api/v1/valuation",
    tags=["Valuation"],
)

app.include_router(
    portfolio.router,
    prefix="/api/v1/portfolio",
    tags=["Portfolio"],
)

app.include_router(
    documents.router,
    prefix="/api/v1/documents",
    tags=["Documents"],
)

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"],
)