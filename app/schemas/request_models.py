from typing import Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3)
    jurisdiction: Optional[str] = None
    category: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)


class QARequest(BaseModel):
    question: str = Field(..., min_length=5)
    jurisdiction: Optional[str] = None
    category: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=20)
    max_words: int = Field(default=250, ge=50, le=1000)


class ComparisonRequest(BaseModel):
    topic: str = Field(..., min_length=5)
    jurisdiction_1: str
    jurisdiction_2: str
    category: str
    top_k: int = Field(default=3, ge=1, le=10)


class ClauseExtractionRequest(BaseModel):
    text: str = Field(..., min_length=20)


class ChecklistRequest(BaseModel):
    topic: str = Field(..., min_length=5)
    jurisdiction: Optional[str] = None
    category: Optional[str] = None
    top_k: int = Field(default=3, ge=1, le=10)