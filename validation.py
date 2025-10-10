"""
Business rule validation for insurance documents.
"""
from datetime import datetime
from typing import List, Set
import logging

from models import ExtractedData, ValidationResult

logger = logging.getLogger(__name__)


class DocumentValidator:
    """Validates extracted insurance document data against business rules."""
    
    def __init__(self, valid_vessels: Set[str]):
        """
        Initialize validator with valid vessel names.
        
        Args:
            valid_vessels: Set of approved vessel names
        """
        self.valid_vessels = valid_vessels
        logger.info(f"Validator initialized with {len(valid_vessels)} valid vessels")
    
    def validate(self, data: ExtractedData) -> List[ValidationResult]:
        """
        Validate extracted data against all business rules.
        
        Args:
            data: ExtractedData object to validate
            
        Returns:
            List of ValidationResult objects
        """
        results = []
        
        # Rule 1: Date Consistency
        results.append(self._validate_date_consistency(data))
        
        # Rule 2: Value Check
        results.append(self._validate_insured_value(data))
        
        # Rule 3: Vessel Name Match
        results.append(self._validate_vessel_name(data))
        
        # Rule 4: Completeness Check
        results.append(self._validate_completeness(data))
        
        return results
    
    def _validate_date_consistency(self, data: ExtractedData) -> ValidationResult:
        """
        Validate that policy_end_date is after policy_start_date.
        
        Args:
            data: ExtractedData object
            
        Returns:
            ValidationResult for date consistency rule
        """
        rule_name = "Date Consistency"
        
        try:
            if not data.policy_start_date or not data.policy_end_date:
                return ValidationResult(
                    rule=rule_name,
                    status="FAIL",
                    message="Missing start or end date."
                )
            
            start_date = datetime.strptime(data.policy_start_date, "%Y-%m-%d")
            end_date = datetime.strptime(data.policy_end_date, "%Y-%m-%d")
            
            if end_date > start_date:
                return ValidationResult(
                    rule=rule_name,
                    status="PASS",
                    message="Policy end date is after start date."
                )
            else:
                return ValidationResult(
                    rule=rule_name,
                    status="FAIL",
                    message=f"Policy end date ({data.policy_end_date}) must be after start date ({data.policy_start_date})."
                )
                
        except ValueError as e:
            logger.error(f"Date parsing error: {e}")
            return ValidationResult(
                rule=rule_name,
                status="FAIL",
                message=f"Invalid date format: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in date validation: {e}")
            return ValidationResult(
                rule=rule_name,
                status="FAIL",
                message=f"Date validation error: {str(e)}"
            )
    
    def _validate_insured_value(self, data: ExtractedData) -> ValidationResult:
        """
        Validate that insured_value is greater than 0.
        
        Args:
            data: ExtractedData object
            
        Returns:
            ValidationResult for value check rule
        """
        rule_name = "Value Check"
        
        try:
            if data.insured_value is None:
                return ValidationResult(
                    rule=rule_name,
                    status="FAIL",
                    message="Insured value is missing."
                )
            
            if data.insured_value > 0:
                return ValidationResult(
                    rule=rule_name,
                    status="PASS",
                    message="Insured value is valid."
                )
            else:
                return ValidationResult(
                    rule=rule_name,
                    status="FAIL",
                    message=f"Insured value ({data.insured_value}) must be greater than 0."
                )
                
        except Exception as e:
            logger.error(f"Error in value validation: {e}")
            return ValidationResult(
                rule=rule_name,
                status="FAIL",
                message=f"Value validation error: {str(e)}"
            )
    
    def _validate_vessel_name(self, data: ExtractedData) -> ValidationResult:
        """
        Validate that vessel_name exists in the approved list.
        
        Args:
            data: ExtractedData object
            
        Returns:
            ValidationResult for vessel name match rule
        """
        rule_name = "Vessel Name Match"
        
        try:
            if not data.vessel_name:
                return ValidationResult(
                    rule=rule_name,
                    status="FAIL",
                    message="Vessel name is missing."
                )
            
            # Case-insensitive comparison
            vessel_name_lower = data.vessel_name.lower()
            valid_vessels_lower = {v.lower() for v in self.valid_vessels}
            
            if vessel_name_lower in valid_vessels_lower:
                return ValidationResult(
                    rule=rule_name,
                    status="PASS",
                    message=f"Vessel '{data.vessel_name}' is on the approved list."
                )
            else:
                return ValidationResult(
                    rule=rule_name,
                    status="FAIL",
                    message=f"Vessel '{data.vessel_name}' is not on the approved list."
                )
                
        except Exception as e:
            logger.error(f"Error in vessel name validation: {e}")
            return ValidationResult(
                rule=rule_name,
                status="FAIL",
                message=f"Vessel validation error: {str(e)}"
            )
    
    def _validate_completeness(self, data: ExtractedData) -> ValidationResult:
        """
        Validate that policy_number is not null or empty.
        
        Args:
            data: ExtractedData object
            
        Returns:
            ValidationResult for completeness check rule
        """
        rule_name = "Completeness Check"
        
        try:
            if data.policy_number and data.policy_number.strip():
                return ValidationResult(
                    rule=rule_name,
                    status="PASS",
                    message="Policy number is present."
                )
            else:
                return ValidationResult(
                    rule=rule_name,
                    status="FAIL",
                    message="Policy number is missing or empty."
                )
                
        except Exception as e:
            logger.error(f"Error in completeness validation: {e}")
            return ValidationResult(
                rule=rule_name,
                status="FAIL",
                message=f"Completeness validation error: {str(e)}"
            )