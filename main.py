from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Document Structurer",
    description="Transforms unstructured text into structured JSON data.",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1")