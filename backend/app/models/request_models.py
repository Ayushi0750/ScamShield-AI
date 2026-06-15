

from pydantic import BaseModel, Field, validator
from typing import Optional


class JobAnalysisRequest(BaseModel):
    job_text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Job description text to analyze for scam detection"
    )

   
    actual_label: Optional[int] = Field(
        None,
        description="Optional ground truth label ID for evaluation (0=GENUINE, 1=SCAM) or any integer index"
    )

    
    @validator("job_text")
    def clean_job_text(cls, value):
        if not value:
            raise ValueError("job_text cannot be empty")

        cleaned = value.strip()

        if len(cleaned) < 10:
            raise ValueError("job_text is too short for analysis")

        return cleaned

    
    @validator("actual_label")
    def validate_label(cls, value):
        if value is None:
            return value
        
       
        if not isinstance(value, int) or value < 0:
            raise ValueError("actual_label must be a non-negative integer or None")
        
        return value