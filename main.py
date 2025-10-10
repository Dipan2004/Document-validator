"""
FastAPI application for insurance document validation.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from models import DocumentRequest, ValidationResponse
from ai_extractor import AIExtractor
from validation import DocumentValidator
from utils import load_valid_vessels

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
ai_extractor = None
validator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown."""
    global ai_extractor, validator
    
    try:
        logger.info("Initializing AI Extractor...")
        ai_extractor = AIExtractor()
        
        logger.info("Loading valid vessels...")
        valid_vessels = load_valid_vessels()
        
        logger.info("Initializing Document Validator...")
        validator = DocumentValidator(valid_vessels)
        
        logger.info("Application startup complete")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise
    finally:
        logger.info("Application shutdown")


app = FastAPI(
    title="Mini Document Validator",
    description="Insurance document validation microservice using Gemini AI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Mini Document Validator",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "ai_extractor": "initialized" if ai_extractor else "not initialized",
        "validator": "initialized" if validator else "not initialized"
    }


@app.post("/validate", response_model=ValidationResponse)
async def validate_document(request: DocumentRequest):
    """
    Validate an insurance document.
    
    Args:
        request: DocumentRequest containing the document text
        
    Returns:
        ValidationResponse with extracted data and validation results
        
    Raises:
        HTTPException: If extraction or validation fails
    """
    if not ai_extractor or not validator:
        logger.error("Service not properly initialized")
        raise HTTPException(
            status_code=500,
            detail="Service not properly initialized. Please try again later."
        )
    
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Document text cannot be empty"
        )
    
    try:
        logger.info("Starting document extraction...")
        
        # Extract data using Gemini AI
        extracted_data = await ai_extractor.extract_fields(request.text)
        
        logger.info(f"Extraction successful: {extracted_data}")
        
        # Validate extracted data
        validation_results = validator.validate(extracted_data)
        
        logger.info(f"Validation complete: {len(validation_results)} rules checked")
        
        return ValidationResponse(
            extracted_data=extracted_data,
            validation_results=validation_results
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during validation: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )