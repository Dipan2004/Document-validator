"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class DocumentRequest(BaseModel):
    """Request model for document validation endpoint."""
    
    text: str = Field(
        ...,
        description="Raw text content of the insurance document",
        min_length=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "This Marine Hull Insurance Policy confirms that the vessel MV Neptune is covered under policy number HM-2025-10-A4B for the period from 1st November 2025 to 31st October 2026. The total insured value is INR 5,000,000."
            }
        }


class ExtractedData(BaseModel):
    """Model for extracted insurance document fields."""
    
    policy_number: Optional[str] = Field(
        None,
        description="Policy number from the document"
    )
    vessel_name: Optional[str] = Field(
        None,
        description="Name of the insured vessel"
    )
    policy_start_date: Optional[str] = Field(
        None,
        description="Policy start date in YYYY-MM-DD format"
    )
    policy_end_date: Optional[str] = Field(
        None,
        description="Policy end date in YYYY-MM-DD format"
    )
    insured_value: Optional[float] = Field(
        None,
        description="Total insured value as a number"
    )
    
    @field_validator('policy_start_date', 'policy_end_date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate that dates are in YYYY-MM-DD format."""
        if v is None:
            return v
        
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError(f"Date must be in YYYY-MM-DD format, got: {v}")
    
    @field_validator('insured_value')
    @classmethod
    def validate_insured_value(cls, v: Optional[float]) -> Optional[float]:
        """Validate that insured_value is a valid number."""
        if v is None:
            return v
        
        if not isinstance(v, (int, float)):
            raise ValueError(f"Insured value must be a number, got: {type(v)}")
        
        return float(v)
    
    class Config:
        json_schema_extra = {
            "example": {
                "policy_number": "HM-2025-10-A4B",
                "vessel_name": "MV Neptune",
                "policy_start_date": "2025-11-01",
                "policy_end_date": "2026-10-31",
                "insured_value": 5000000.0
            }
        }


class ValidationResult(BaseModel):
    """Model for individual validation rule result."""
    
    rule: str = Field(
        ...,
        description="Name of the validation rule"
    )
    status: str = Field(
        ...,
        description="Status of the validation (PASS/FAIL)",
        pattern="^(PASS|FAIL)$"
    )
    message: str = Field(
        ...,
        description="Detailed message about the validation result"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "rule": "Date Consistency",
                "status": "PASS",
                "message": "Policy end date is after start date."
            }
        }


class ValidationResponse(BaseModel):
    """Response model for document validation endpoint."""
    
    extracted_data: ExtractedData = Field(
        ...,
        description="Data extracted from the document"
    )
    validation_results: List[ValidationResult] = Field(
        ...,
        description="Results of all validation rules"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "extracted_data": {
                    "policy_number": "HM-2025-10-A4B",
                    "vessel_name": "MV Neptune",
                    "policy_start_date": "2025-11-01",
                    "policy_end_date": "2026-10-31",
                    "insured_value": 5000000.0
                },
                "validation_results": [
                    {
                        "rule": "Date Consistency",
                        "status": "PASS",
                        "message": "Policy end date is after start date."
                    },
                    {
                        "rule": "Value Check",
                        "status": "PASS",
                        "message": "Insured value is valid."
                    },
                    {
                        "rule": "Vessel Name Match",
                        "status": "PASS",
                        "message": "Vessel 'MV Neptune' is on the approved list."
                    },
                    {
                        "rule": "Completeness Check",
                        "status": "PASS",
                        "message": "Policy number is present."
                    }
                ]
            }
        }