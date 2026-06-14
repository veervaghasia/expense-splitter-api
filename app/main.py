from contextlib import asynccontextmanager # For managing lifespan events in FastAPI

from fastapi import FastAPI

# Import DB setup function
from app.db import create_db_and_tables

# Import router
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Rins once when application starts.
    """

    create_db_and_tables()  # Ensure tables are created before handling requests

    # Everything before yield runs at startup
    yield

    # Everything after yield runs at shutdown
    # (nothing needed for now)


app = FastAPI(lifespan=lifespan)

app.include_router(router)  # Register our API routes with the main app


@app.get("/")
def root():
    return {
        "message": "Expense Splitter API Running!"
    }
