from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
import logging
import sys
from pydantic import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import API routers
from src.api.chatbot import router as chatbot_router

app = FastAPI(
    title="AI Textbook RAG Chatbot API",
    description="API for interacting with the AI-Native Textbook using RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chatbot_router, prefix="/api", tags=["chatbot"])

@app.get("/")
def read_root():
    return {"message": "AI Textbook RAG Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request, exc):
    logger.error(f"Pydantic validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    logger.info("Starting AI Textbook RAG Chatbot API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)