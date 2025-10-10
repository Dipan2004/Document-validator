"""
AI-powered field extraction using Google Gemini API.
"""
import os
import json
import logging
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

from models import ExtractedData

load_dotenv()

logger = logging.getLogger(__name__)


class AIExtractor:
    """Handles AI-based extraction of fields from insurance documents."""
    
    def __init__(self):
        """Initialize the Gemini AI model."""
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please set it in your .env file."
            )
        
        try:
            genai.configure(api_key=api_key)
            
            # Configure model for JSON output
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-latest",
                generation_config={
                    "temperature": 0.1,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                    "response_mime_type": "application/json",
                }
            )
            
            logger.info("Gemini AI model initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {e}")
            raise ValueError(f"Failed to initialize Gemini API: {str(e)}")
    
    def _build_prompt(self, document_text: str) -> str:
        """
        Build the extraction prompt for Gemini.
        
        Args:
            document_text: Raw text from the insurance document
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert insurance document parser.
Extract and return only the following fields from the provided insurance document text in strict JSON format:
{{
  "policy_number": "...",
  "vessel_name": "...",
  "policy_start_date": "YYYY-MM-DD",
  "policy_end_date": "YYYY-MM-DD",
  "insured_value": number
}}

Rules:
- Extract dates in YYYY-MM-DD format
- Convert insured_value to a numeric value (remove currency symbols and commas)
- If a field cannot be found, use null
- Return ONLY valid JSON, no explanations or markdown

Document text:
{document_text}

Return ONLY valid JSON."""
        
        return prompt
    
    async def extract_fields(self, document_text: str) -> ExtractedData:
        """
        Extract insurance fields from document text using Gemini AI.
        
        Args:
            document_text: Raw text from the insurance document
            
        Returns:
            ExtractedData object with parsed fields
            
        Raises:
            ValueError: If extraction fails or returns invalid data
        """
        try:
            prompt = self._build_prompt(document_text)
            
            logger.info("Sending extraction request to Gemini AI...")
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise ValueError("Empty response received from Gemini AI")
            
            logger.debug(f"Raw AI response: {response.text}")
            
            # Parse JSON response
            try:
                extracted_dict = json.loads(response.text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {response.text}")
                raise ValueError(f"Invalid JSON response from AI: {str(e)}")
            
            # Validate and convert to ExtractedData model
            try:
                extracted_data = ExtractedData(**extracted_dict)
                logger.info("Successfully extracted and validated data")
                return extracted_data
                
            except Exception as e:
                logger.error(f"Failed to validate extracted data: {e}")
                raise ValueError(f"Extracted data validation failed: {str(e)}")
            
        except ValueError:
            # Re-raise validation errors
            raise
            
        except Exception as e:
            logger.error(f"Unexpected error during extraction: {e}", exc_info=True)
            raise ValueError(f"AI extraction failed: {str(e)}")
    
    def extract_fields_sync(self, document_text: str) -> ExtractedData:
        """
        Synchronous version of extract_fields for testing.
        
        Args:
            document_text: Raw text from the insurance document
            
        Returns:
            ExtractedData object with parsed fields
        """
        try:
            prompt = self._build_prompt(document_text)
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise ValueError("Empty response received from Gemini AI")
            
            extracted_dict = json.loads(response.text)
            extracted_data = ExtractedData(**extracted_dict)
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"Synchronous extraction failed: {e}")
            raise ValueError(f"AI extraction failed: {str(e)}")