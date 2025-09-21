# backend/app/models.py
from pydantic import BaseModel
from typing import List


class TrendRequest(BaseModel):
query: str
location: str | None = None


class TrendResponse(BaseModel):
query: str
top_skills: List[str]
confidence_scores: List[float]
district_heatmap_data: dict