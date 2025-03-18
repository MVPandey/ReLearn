from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.logger import logger
from app.api.agents import router as agents_router

app = FastAPI(
    title="Relearn API",
    description="API for Relearn application",
    version="0.0.1",
    logger=logger,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=logger,
        log_level="info",
        access_log=True,
    )
