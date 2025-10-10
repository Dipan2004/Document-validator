"""
Utility functions for the application.
"""
import json
import logging
from pathlib import Path
from typing import Set

logger = logging.getLogger(__name__)


def load_valid_vessels(filename: str = "valid_vessels.json") -> Set[str]:
    """
    Load valid vessel names from JSON file.
    
    Args:
        filename: Path to the valid vessels JSON file
        
    Returns:
        Set of valid vessel names
        
    Raises:
        FileNotFoundError: If the vessels file doesn't exist
        ValueError: If the file contains invalid JSON or structure
    """
    filepath = Path(filename)
    
    if not filepath.exists():
        logger.error(f"Valid vessels file not found: {filepath}")
        raise FileNotFoundError(
            f"Valid vessels file not found: {filepath}. "
            "Please ensure valid_vessels.json exists in the project root."
        )
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            vessels_data = json.load(f)
        
        if not isinstance(vessels_data, list):
            raise ValueError("Valid vessels file must contain a JSON array")
        
        if not all(isinstance(v, str) for v in vessels_data):
            raise ValueError("All vessel names must be strings")
        
        vessels_set = set(vessels_data)
        logger.info(f"Loaded {len(vessels_set)} valid vessels from {filename}")
        
        return vessels_set
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in vessels file: {e}")
        raise ValueError(f"Invalid JSON in valid_vessels.json: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error loading valid vessels: {e}")
        raise


def format_currency(value: float, currency: str = "INR") -> str:
    """
    Format a numeric value as currency.
    
    Args:
        value: Numeric value to format
        currency: Currency code (default: INR)
        
    Returns:
        Formatted currency string
    """
    if value is None:
        return "N/A"
    
    try:
        if currency == "INR":
            # Indian numbering system (lakhs and crores)
            return f"INR {value:,.2f}"
        else:
            return f"{currency} {value:,.2f}"
    except Exception as e:
        logger.warning(f"Error formatting currency: {e}")
        return f"{currency} {value}"


def sanitize_text(text: str, max_length: int = 10000) -> str:
    """
    Sanitize and truncate input text.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes and other control characters
    sanitized = ''.join(char for char in text if char.isprintable() or char.isspace())
    
    # Truncate if too long
    if len(sanitized) > max_length:
        logger.warning(f"Text truncated from {len(sanitized)} to {max_length} characters")
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()


def validate_api_key(api_key: str) -> bool:
    """
    Validate that an API key has a reasonable format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if the key appears valid, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # Basic validation: key should be at least 20 characters
    if len(api_key.strip()) < 20:
        return False
    
    return True